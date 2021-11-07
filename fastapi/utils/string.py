import random
import string
from fastapi import HTTPException
from config.conf import IMAGES_UPLOAD_PATH
from datetime import datetime


def random_string(length: int = 64) -> str:
    return ''.join(
        random.choice(
            string.ascii_uppercase + string.digits + string.ascii_lowercase
        ) for _ in range(length)
    )


def generate_image_name(content_type: str, with_path=True):
    types = {"image/png": "png", "image/jpeg": "jpeg"}

    if content_type not in types.keys():
        raise HTTPException(400, "formato file non supportato")

    ext = types[content_type]

    filename = ".".join([
        str(round(datetime.now().timestamp()*1000)),
        random_string(3),
        ext
    ])
    dest_path = IMAGES_UPLOAD_PATH / filename
    return dest_path if with_path else filename


def generate_image_name_b64(filename: str,  with_path=True):
    extension = filename.split('.').pop()

    file_name = ".".join([
        str(round(datetime.now().timestamp()*1000)),
        random_string(3),
        extension
    ])

    dest_path = IMAGES_UPLOAD_PATH / file_name
    return dest_path if with_path else file_name
