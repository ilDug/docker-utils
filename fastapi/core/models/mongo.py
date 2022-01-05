from pydantic import BaseModel, BaseConfig, Field
from datetime import datetime
from bson import ObjectId
from uuid import UUID


class OId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid mongo objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class MongoModel(BaseModel):
    # id: OId = Field(None, alias="_id")

    class Config:
        json_encoders = {
            datetime: lambda dt: dt.isoformat(),
            ObjectId: lambda oid: str(oid),
            UUID: lambda uuid: str(uuid),
        }
        extra = "allow"
        allow_population_by_field_name = True
