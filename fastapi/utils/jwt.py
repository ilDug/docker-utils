from typing import Union
from pydantic.types import UUID5
from models.account import JWTModel
import uuid
from time import time
from datetime import datetime, timedelta
from pathlib import Path
from config.conf import JWT_KEY_PATH, JWT_CERT_PATH
import jwt
from cryptography.x509 import load_pem_x509_certificate
from fastapi import HTTPException


class JWT():
    rsa_crt_path: Path = JWT_CERT_PATH
    rsa_JWT_KEY_PATH: Path = JWT_KEY_PATH
    JWT_NAMESPACE: uuid.UUID = uuid.UUID(
        "69d3e8f4-0872-4f7f-9f35-d2ee437e0887")

    @classmethod
    def jti(cls, uid: str) -> str:
        now = round(time() * 1000)
        return str(uuid.uuid5(cls.JWT_NAMESPACE, str(uid) + str(now)))

    @classmethod
    def base_payload(cls, duration: int) -> dict:
        now = datetime.utcnow()
        nbf = {"nbf": now}
        iat = {"iat": now}
        exp = {"exp": now + timedelta(days=duration)}
        payload = {**nbf, **iat, **exp}
        return payload

    @classmethod
    def create(cls, user: dict, duration=30) -> str:
        try:
            jti = {"jti": cls.jti(user['uid'])}
            key = cls.rsa_JWT_KEY_PATH.read_text()
            payload = cls.base_payload(duration)
            payload = {**payload, **user, **jti}
            token = jwt.encode(payload, key, algorithm="RS256")
            return token
        except Exception as e:
            raise HTTPException(500, "JWT error DAG: " + str(e))

    @classmethod
    def verify(cls, token: str) -> JWTModel:
        try:
            crt = cls.rsa_crt_path.read_text()
            cert_obj = load_pem_x509_certificate(crt.encode())
            public_key = cert_obj.public_key()
            # private_key = cert_obj.private_key()
            decoded = jwt.decode(token, public_key, algorithms=["RS256"])
            return JWTModel(**decoded)
        except Exception as e:
            raise HTTPException(500, "JWT verify error DAG: " + str(e))
