# from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.cors import CORSMiddleware
from typing import Optional
from fastapi import FastAPI, Header, Request
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.responses import PlainTextResponse
from fastapi.staticfiles import StaticFiles
from pymongo.errors import PyMongoError

from config.conf import ASSETS_PATH
from account.routers import account_router, auth_router

from core.middlewares.exception_handlers import (
    req_validation_error_handler,
    dag_http_error_handler,
    mongo_error_handler,
)

app = FastAPI(root_path="/api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    # allow_origins=["http://127.0.0.1"],
    allow_credentials=True,
    allow_methods=["OPTION", "POST", "PUT", "GET", "DELETE"],
    allow_headers=["*", "x-error"],
    expose_headers=["*"],
)

app.add_exception_handler(RequestValidationError, req_validation_error_handler)
app.add_exception_handler(HTTPException, dag_http_error_handler)
app.add_exception_handler(PyMongoError, mongo_error_handler)

app.include_router(account_router)
app.include_router(auth_router)

app.mount("/assets", StaticFiles(directory=ASSETS_PATH), name="static_media")


@app.get("/", response_class=PlainTextResponse)
async def root():
    return "API SERVER RUNNING..."
