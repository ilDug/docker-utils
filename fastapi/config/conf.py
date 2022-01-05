from decouple import config
from pathlib import Path


# MONGO
###############################
MONGO_USER_PW = config("MONGO_USER_PW")
MONGO_USER_NAME = config("MONGO_USER_NAME")
MONGO_DB = config("MONGO_DB")
MONGO_HOST = config("MONGO_HOST")
MONGO_PORT = config("MONGO_PORT")
MONGO_CS = f"mongodb://{MONGO_USER_NAME}:{MONGO_USER_PW}@{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB}?authSource=admin"

# EMAIL
###############################
MAIL_CONFIG = {
    "host": config("MAIL_HOST"),
    "port": config("MAIL_PORT", cast=int),
    "user": config("MAIL_USER"),
    "password": config("MAIL_PW"),
}

EMAIL_TEMPLATE_BASE = Path(__file__).parent / "../lib/templates/base-template.html"
EMAIL_TEMPLATE_ACTIVATION = (
    Path(__file__).parent / "../lib/templates/user-activation.html"
)
EMAIL_TEMPLATE_RECOVER = (
    Path(__file__).parent / "../lib/templates/recover-password.html"
)


# JWT
###############################
JWT_KEY_PATH = Path(__file__).parent / "../lib/keys/auth.key"
JWT_CERT_PATH = Path(__file__).parent / "../lib/certs/auth.crt"
ACTIVATION_KEY_LENGTH = config("ACTIVATION_KEY_LENGTH", cast=int)


# IMAGES AND MEDIA
###############################
ASSETS_PATH = Path(__file__).parent / "../assets"
IMAGES_UPLOAD_PATH = ASSETS_PATH / "images/upload"
