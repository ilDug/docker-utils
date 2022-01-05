import hashlib

from datetime import datetime
from fastapi import HTTPException
from pymongo import MongoClient

from account.models import UserModel, UserOperation
from account.controllers import Account
from config.conf import ACTIVATION_KEY_LENGTH, MONGO_CS


#############################################################################################
#################  ACCOUNT ACTIVATION    ####################################################
#############################################################################################


class AccountActivation(Account):
    def __init__(self):
        super().__init__()

    # attiva l'account
    def activate(self, key: str) -> bool:
        if not key or len(key) != ACTIVATION_KEY_LENGTH:
            raise HTTPException(400, "invalid activation link")

        with MongoClient(MONGO_CS) as c:
            with c.start_session() as s:
                with s.start_transaction():
                    activation = c.shop.operations.find_one({"key": key})
                    if activation is None:
                        raise HTTPException(400, "chiave di attivazione inesistente")
                    activation = UserOperation(**activation)

                    user = c.shop.users.find_one({"uid": str(activation.uid)})
                    user = UserModel(**user)
                    if user.active:
                        raise HTTPException(400, "utente già attivo")

                    if activation.scope != self.ACTIVATION_SCOPE:
                        raise HTTPException(
                            400,
                            "la chiave fornita non e' adatta per l'attivazione dell'account",
                        )

                    res = c.shop.users.update_one(
                        {"uid": str(activation.uid)}, {"$set": {"active": True}}
                    ).modified_count
                    if res <= 0:
                        raise HTTPException(
                            500, str("Errore attivazione account SET ACTIVE ERROR")
                        )

                    res = c.shop.operations.update_one(
                        {"_id": activation._id},
                        {"$set": {"used_at": datetime.utcnow()}},
                    ).modified_count

                    if res <= 0:
                        raise HTTPException(
                            500, str("Errore attivazione account ACTIVATION DATE ERROR")
                        )
                    return True

    def resend_activation_email(self, email_hash: str):
        pass
        with MongoClient(MONGO_CS) as c:
            user: UserModel = None
            users = c.shop.users.find({})
            for u in users:
                if email_hash == hashlib.md5(u["email"].encode()).hexdigest():
                    user = UserModel(**u)
                    break

            if user is None:
                raise HTTPException(
                    400, "email non trovata, esegui prima la registrazione"
                )

            if user.active:
                raise HTTPException(400, "utente già attivo")

            activations = [
                a
                for a in c.shop.operations.find(
                    {"uid": user.uid, "scope": self.ACTIVATION_SCOPE}
                )
                .sort([("created_at", -1)])
                .limit(1)
            ]
            activation = UserOperation(**activations[0])

            return self.send_activation_email(user.email, activation.key)
