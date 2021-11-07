from typing import Optional
from fastapi.param_functions import Path
from controllers.auth import Auth
from fastapi import HTTPException, APIRouter, Header, Query, routing

router = APIRouter(tags=['auth'])


@router.get("/auth/authenticate")
async def authenticate(authorization: str = Header(None), claims: Optional[bool] = Query(False)):
    return Auth().authenticate(authorization, claims=claims)


@router.get("/auth/authorization/check/permission/{permission}")
async def authorization_check(authorization: str = Header(None), permission: str = Path(...)):
    return Auth().authorize(authorization, permission)
