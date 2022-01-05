import uuid
import hashlib
import bcrypt
import json

from string import Template
from datetime import datetime
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import IPvAnyAddress
from pymongo import MongoClient
from bson import json_util

from core.models import MongoModel
from account.models import JWTModel, UserModel
from core import DagMail, DagMailConfig
from account.jwt import JWT
from core.utils.string import random_string
from config.conf import (
    MONGO_CS,
    ACTIVATION_KEY_LENGTH,
    EMAIL_TEMPLATE_ACTIVATION,
    EMAIL_TEMPLATE_BASE,
    MAIL_CONFIG,
)


class Account:
    UUID_NAMESPACE = uuid.UUID("9711c6f0-b5a2-11eb-9e14-c82a1456945d")
    ACTIVATION_SCOPE = "account_activation"

    def __init__(self):
        pass

    # si connette al server e restituisce il token JWT
    def login(self, email: str, password: str, ip: IPvAnyAddress = None):
        if not email:
            raise HTTPException(400, "il campo email non è specificato")

        if not password:
            raise HTTPException(400, "la richiesta non contiene la password")

        email = email.lower().strip()

        # controlla che l'utente sia presente nel database
        with MongoClient(MONGO_CS) as c:
            user = c.shop.users.find_one({"email": email})

            if user is None:
                raise HTTPException(
                    404,
                    "Utente non registrato. Procedi prima con la registrazione del tuo account.",
                )
            user = UserModel(**user)

            # verifica la password
            if not bcrypt.checkpw(password.encode(), user.hashed_password.encode()):
                raise HTTPException(500, "password non corretta per questo account.")

            # crea il token filtrando i dati sensibili
            token: str = JWT.create(
                user.dict(exclude={"id", "hashed_password", "registration_date"})
            )
            jwt: JWTModel = JWT.verify(token)

            # inserisce il token nel database assieme ai dati del login
            access = c.shop.accesses.insert_one(
                {
                    "uid": str(jwt.uid),
                    "jti": str(jwt.jti),
                    "ip": ip,
                    "date": datetime.utcnow(),
                }
            ).inserted_id
            if access is None:
                raise HTTPException(
                    500,
                    "Errore,  si sono verificati problemi con la connsessione al server, riprovare più tardi",
                )
            return str(token)

    # registra l'utente e  rotrna il token JWT
    def register(self, email: str, password: str, ip: IPvAnyAddress = None) -> str:
        if not email:
            raise HTTPException(400, "il campo email non è specificato")

        if not password:
            raise HTTPException(400, "la richiesta non contiene la password")

        email = email.lower().strip()
        # controlla che l'utente esista
        email_hash = hashlib.md5(email.encode()).hexdigest()
        if self.exists(email_hash):
            raise HTTPException(
                400, "un utente con questa email esiste gia' nel database"
            )
        salt = bcrypt.gensalt()
        hashed_pw = bcrypt.hashpw(password.encode(), salt).decode()
        uid = uuid.uuid5(self.UUID_NAMESPACE, email)

        with MongoClient(MONGO_CS) as c:
            with c.start_session() as s:
                with s.start_transaction() as t:

                    # cerca se la chiave di attivazione esiste
                    while True:
                        activation_key = random_string(ACTIVATION_KEY_LENGTH)
                        if c.shop.operations.find_one({"key": activation_key}) is None:
                            break

                    # inserisce il nuovo utente
                    id = c.shop.users.insert_one(
                        {
                            "uid": str(uid),
                            "email": email,
                            "active": False,
                            "authorizations": ["basic"],
                            "hashed_password": hashed_pw,
                            "registration_date": datetime.now(),
                        }
                    ).inserted_id

                    if id is None:
                        raise HTTPException(500, str("errore inserimento nuovo utente"))

                    # genera una chiave di attivazione e la inserisce
                    id = c.shop.operations.insert_one(
                        {
                            "uid": str(uid),
                            "key": activation_key,
                            "created_at": datetime.utcnow(),
                            "used_at": None,
                            "scope": self.ACTIVATION_SCOPE,
                        }
                    ).inserted_id

                    if id is None:
                        raise HTTPException(
                            500, "errore generazione chiave di attivazione"
                        )

                    # manda la mail di attivazione
                    if not self.send_activation_email(email, activation_key):
                        raise HTTPException(500, "errori di invio email di attivazione")

                return self.login(email, password, ip)

    def exists(self, email_hash: str) -> bool:
        with MongoClient(MONGO_CS) as c:
            emails = [
                hashlib.md5(e["email"].encode()).hexdigest()
                for e in c.shop.users.find({}, {"email": 1, "_id": 0})
            ]

        return email_hash in emails

    # manda la email cn il codice di attivazione edell'account
    # @return boolean se la mail è stata invata

    def send_activation_email(self, email: str, activation_key: str) -> bool:
        content_template = EMAIL_TEMPLATE_ACTIVATION.read_text()
        content = Template(content_template).substitute(ACTIVATION_KEY=activation_key)
        body_template = EMAIL_TEMPLATE_BASE.read_text()
        body = Template(body_template).substitute(CONTENT=content)
        try:
            config = DagMailConfig(**MAIL_CONFIG)
            with DagMail(config) as ms:
                ms.add_receiver(email)
                ms.messageHTML(body, "Attivazione Account")
                ms.send()
                return True
        except Exception as e:
            print(str(e))
            return False
