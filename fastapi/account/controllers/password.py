import bcrypt

from string import Template
from email_validator import validate_email
from datetime import datetime, timedelta
from fastapi import HTTPException
from pymongo import MongoClient

from core import DagMail, DagMailConfig
from core.utils.string import random_string
from account.models import UserModel, UserOperation
from account.controllers import Account
from config.conf import (
    EMAIL_TEMPLATE_BASE,
    EMAIL_TEMPLATE_RECOVER,
    MAIL_CONFIG,
    MONGO_CS,
    ACTIVATION_KEY_LENGTH,
)

#############################################################################################
#################  PASSWORD #################################################################
#############################################################################################


class Password(Account):
    RECOVER_SCOPE = "recover_password"

    def __init__(self):
        super().__init__()

    # genera una chiave di attivazione che permette di ripristinare la password
    # restituisce la key via email
    def recover(self, email: str) -> bool:
        if not email:
            raise HTTPException(400, "il campo email non è specificato")
        try:
            validate_email(email)
        except Exception as e:
            raise HTTPException(400, "indirizzo email non valido")
        email = email.lower().strip()

        with MongoClient(MONGO_CS) as c:
            user = c.shop.users.find_one({"email": email})
            if user is None:
                raise HTTPException(400, "indirizzo email non presente nel database")
            user = UserModel(**user)

            # cerca se la chiave di attivazione esiste
            while True:
                recover_key = random_string(ACTIVATION_KEY_LENGTH)
                if c.shop.operations.find_one({"key": recover_key}) is None:
                    break

            id = c.shop.operations.insert_one(
                {
                    "uid": user.uid,
                    "key": recover_key,
                    "created_at": datetime.utcnow(),
                    "used_at": None,
                    "scope": self.RECOVER_SCOPE,
                }
            ).inserted_id

            if id is None:
                raise HTTPException(500, "Errore creazione chiave di recupero")

            # manda l'email di recover password
            if not self.send_recover_email(email, recover_key):
                raise HTTPException(
                    500, "Errore nell recupero della password,  prova più tardi"
                )

            return True

    # esegui i controlli della chiave e restituisce l'uid dell'utente per
    # procedere con il set della password

    def restore_init(self, key: str) -> str:
        if not key or len(key) != ACTIVATION_KEY_LENGTH:
            raise HTTPException(
                400, "la richiesta non contiene la chiave di attivazione corretta"
            )

        with MongoClient(MONGO_CS) as c:
            sql = "SELECT * FROM activations WHERE activationKey = %s"
            r = c.shop.operations.find_one({"key": key})
            if not r:
                raise HTTPException(500, "chiave di recupero inesistente")
            operation = UserOperation(**r)

            if operation.scope != self.RECOVER_SCOPE:
                raise HTTPException(
                    400,
                    "la chiave fornita non e' adatta per il recupero della password",
                )

            if operation.used_at is not None:
                raise HTTPException(400, "la chiave fornita e' gia' stata utilizzata")

            limit_date = operation.created_at + timedelta(hours=1)
            if datetime.utcnow() > limit_date:
                raise HTTPException(400, "la chiave fornita e' scaduta")

            return str(operation.uid)

    # impostala nuova password
    # ritorna BOOL

    def restore_set(self, key: str, newpassword: str) -> bool:
        if not newpassword:
            raise HTTPException(400, "la richiesta non contiene la password")

        if not key or len(key) != ACTIVATION_KEY_LENGTH:
            raise HTTPException(400, "invalid recover link")

        # esegue di nuovo i controlli per la chiave
        uid = self.restore_init(key)
        if not uid:
            raise HTTPException(500, "identificativo dell'utente non trovato")

        with MongoClient(MONGO_CS) as c:
            salt = bcrypt.gensalt()
            hashed_pw = bcrypt.hashpw(newpassword.encode(), salt).decode()
            res = c.shop.users.update_one(
                {"uid": uid}, {"$set": {"hashed_password": hashed_pw}}
            ).modified_count
            if res <= 0:
                raise HTTPException(
                    500, "errore nell'impostazione della nuova password"
                )

            res = c.shop.operations.update_one(
                {"key": key}, {"$set": {"used_at": datetime.utcnow()}}
            ).modified_count
            if res <= 0:
                raise HTTPException(500, "errore aggiornamento della chiave")

            return True

    # manda la email cn il codice di attivazione edell'account
    # @return boolean se la mail è stata invata
    def send_recover_email(self, email: str, recover_key: str) -> bool:
        content_template = EMAIL_TEMPLATE_RECOVER.read_text()
        content = Template(content_template).substitute(RECOVER_KEY=recover_key)
        body_template = EMAIL_TEMPLATE_BASE.read_text()
        body = Template(body_template).substitute(CONTENT=content)
        try:
            config = DagMailConfig(**MAIL_CONFIG)
            with DagMail(config) as ms:
                ms.add_receiver(email)
                ms.messageHTML(body, "Recupero password")
                ms.send()
                return True
        except Exception as e:
            print(str(e))
            return False
