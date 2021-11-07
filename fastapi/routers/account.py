from typing import Optional
from pydantic.networks import EmailStr
from starlette.requests import Request
from controllers.account import Account
from controllers.password import Password
from controllers.activation import AccountActivation
from fastapi import APIRouter, Body, Query, Path, Depends, Header
from fastapi.responses import PlainTextResponse
from models.account import PasswordRestoreKeychain, UserRegister, UserLogin

router = APIRouter(tags=['account'])


@router.post('/account/login', response_class=PlainTextResponse)
async def login(req: Request, user: UserLogin = Body(...), x_real_ip: Optional[str] = Header(None)):
    account = Account()
    # ip = req.client.host
    # print(ip, x_real_ip)
    return account.login(**user.dict(), ip=x_real_ip)


# @router.post('/account/register', response_class=PlainTextResponse, dependencies=[Depends(authentication)])
@router.post('/account/register', response_class=PlainTextResponse)
async def register(req: Request, user: UserRegister = Body(...), x_real_ip: Optional[str] = Header(None)):
    account = Account()
    # ip = req.client.host
    return account.register(**user.dict(), ip=x_real_ip)


@router.get('/account/activate/{key}')
async def activate(key: str):
    account = AccountActivation()
    return account.activate(key)


@router.get("/account/resend-activation/{email_md5_hash}")
# 74b328154b0c716ed8fbd2221eb88b0b
async def resend(email_md5_hash: str = Path(..., min_length=32, max_length=32)):
    account = AccountActivation()
    return account.resend_activation_email(email_md5_hash)


@router.get("/account/exists/{email_md5_hash}")
async def user_exists(email_md5_hash: str = Path(...)):
    account = Account()
    return account.exists(email_md5_hash)


@router.post("/account/password/recover", description="genera una chiave di attivazione che permette di ripristinare la password")
async def password_recover(email=Body(..., example="dag@flatmac.com")):
    pw = Password()
    print(email['email'])
    return pw.recover(email['email'])


@router.get("/account/password/restore/init/{key}", description="esegue i controlli per la reimpostazione della password utente")
async def password_restore_init(key: str = Path(...)):
    pw = Password()
    return pw.restore_init(key)


@router.post("/account/password/restore/set", description="imposta la nuova password")
async def password_restore_set(keychain: PasswordRestoreKeychain):
    pw = Password()
    return pw.restore_set(keychain.key, keychain.newpassword)
