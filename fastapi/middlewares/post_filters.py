from typing import Optional
from fastapi import Request, Query

from controllers.auth import Auth


async def hidden_posts(request: Request):
    authorization_header = request.headers['authorization'] if 'authorization' in request.headers else None
    try:
        authorized = Auth().authorize(authorization_header, 'admin')
        return authorized
    except Exception as e:
        return False
