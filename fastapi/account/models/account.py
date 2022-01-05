from config.conf import ACTIVATION_KEY_LENGTH
from datetime import datetime
from pydantic import BaseModel, EmailStr, UUID5, Field, BaseConfig
from typing import List, Optional
from core.models import MongoModel, OId
from email_validator import EmailNotValidError, validate_email


class UserModel(MongoModel):
    id: OId = Field(None, alias="_id")
    # res = db.users.insert_one(user.dict(by_alias=True, exclude={'hashed_password', 'registration_date'}))
    # user.id = res.inserted_id
    uid: str
    email: EmailStr
    active: bool = Field(False)
    authorizations: List[str] = Field([])

    hashed_password: Optional[str] = None
    registration_date: Optional[datetime] = None
    username: Optional[str] = None

    _pj = {"hashed_password": 0, "registration_date": 0}

    # def dict(self):
    #     user_dict = super().dict()
    #     user_dict['uid'] = str(user_dict['uid'])


class JWTModel(MongoModel):
    nbf: datetime
    iat: datetime
    exp: datetime
    jti: UUID5
    email: EmailStr
    authorizations: List[str]
    uid: Optional[UUID5]


class UserOperation(MongoModel):
    uid: UUID5
    key: str = Field(
        ..., min_length=ACTIVATION_KEY_LENGTH, max_length=ACTIVATION_KEY_LENGTH
    )
    created_at: datetime
    used_at: Optional[datetime]
    scope: str


# Modello UTENTE in fase di login
class UserLogin(BaseModel):
    email: EmailStr = Field(..., title="email dell'utente", example="dag@flatmac.com")
    password: str = Field(..., example="adsads")


# modello UTENTE in fase di registrazione
class UserRegister(BaseModel):
    email: EmailStr = Field(
        ..., title="email dell'utente da registrare", example="dag@flatmac.com"
    )
    password: str = Field(example="adsads")


class PasswordRestoreKeychain(BaseModel):
    key: str = Field(
        ..., min_length=ACTIVATION_KEY_LENGTH, max_length=ACTIVATION_KEY_LENGTH
    )
    newpassword: str
