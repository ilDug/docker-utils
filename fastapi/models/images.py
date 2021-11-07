from pydantic import BaseModel


class ImageB64UploadRequestModel(BaseModel):
    filename: str
    base64: str
