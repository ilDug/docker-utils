from fastapi import Request, HTTPException
from fastapi.responses import PlainTextResponse
from fastapi.exceptions import RequestValidationError
from pymongo.errors import PyMongoError


async def req_validation_error_handler(req: Request, exc: RequestValidationError):
    """cattura tutti gli errori di validazione"""

    print("catch DAG REQUEST VALIDATOR ERROR...")
    errors = [e["msg"] for e in exc.errors()]

    return PlainTextResponse(
        content=str(exc), status_code=400, headers={"X-Error": errors[0]}
    )


async def dag_http_error_handler(req: Request, exc: HTTPException):
    """Cattura tutti gli errori per poi poterli restituire come status code nella Response del server"""

    print("catch DAG HTTP ERROR...")
    print(exc)
    return PlainTextResponse(
        content=str(exc.detail),
        status_code=exc.status_code,
        headers={"X-Error": str(exc.detail)},
    )


async def mongo_error_handler(req: Request, exc: PyMongoError):
    print("catch MONGO ERROR (by DAG): ")

    return PlainTextResponse(
        content=str(exc), status_code=500, headers={"X-Error": str(exc)}
    )
