from utils.jwt import JWT
from fastapi import HTTPException


class Auth():
    def __init__(self) -> None:
        pass

    @classmethod
    def authenticate(cls, auth_header: str, claims: bool = False):
        if not auth_header:
            raise HTTPException(
                401, "Unauthorized - l'header non contiene il valore Authorization")

        if not auth_header.startswith("Bearer "):
            raise HTTPException(401, "Unauthorized - l'header non è valido")

        token = auth_header.replace("Bearer ", "")
        try:
            jwt = JWT.verify(token)
        except Exception as e:
            raise HTTPException(
                401, "Unauthorized - il token non è valido")

        return jwt.dict() if claims else True

    def authorize(cls, auth_header: str, permission: str):
        claims = cls.authenticate(auth_header, claims=True)
        if permission in claims['authorizations']:
            return True
        else:
            raise HTTPException(
                401, "Unauthorized for permission: " + permission)
