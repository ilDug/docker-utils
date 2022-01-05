import random
import string
from fastapi import HTTPException
from datetime import datetime


def random_string(length: int = 64) -> str:
    return "".join(
        random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase)
        for _ in range(length)
    )


def generate_image_name(content_type: str, path=""):
    types = {"image/png": "png", "image/jpeg": "jpeg"}

    if content_type not in types.keys():
        raise HTTPException(400, "formato file non supportato")

    ext = types[content_type]

    filename = ".".join(
        [str(round(datetime.now().timestamp() * 1000)), random_string(3), ext]
    )

    name = path + "/" + filename
    return name


def generate_image_name_b64(filename: str, path=""):
    extension = filename.split(".").pop()

    file_name = ".".join(
        [str(round(datetime.now().timestamp() * 1000)), random_string(3), extension]
    )

    name = path + "/" + file_name
    return name
