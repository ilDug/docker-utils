from datetime import datetime
from typing import Optional
from models.mongo import MongoModel
from pydantic import BaseModel, Field
from models.mongo import MongoModel, OId


class PostModel(MongoModel):
    _id: OId = Field(None)
    postid: int = Field(None)
    title: str
    url: str
    hidden: bool


class PostViewModel(MongoModel):
    _id: OId = Field(None)
    postid: int = Field(None)
    date: datetime = Field(None)
    ip: Optional[str] = Field('None')
