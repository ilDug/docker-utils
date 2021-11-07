from decouple import config
from pathlib import Path


# MONGO
###############################

MONGO_AUTH = "mongodb://authuser:xxxxxxx@mongo/users"
MONGO_BLOG = "mongodb://bloguser:xxxxxxx@mongo/blog"

# EMAIL
###############################
MAIL_CONFIG = {
    "host": config('MAIL_HOST'),
    "port": config('MAIL_PORT', cast=int),
    "user": config('MAIL_USER'),
    "password": config('MAIL_PW')
}
EMAIL_TEMPLATE_BASE = Path(__file__).parent / \
    "../lib/templates/base-template.html"

EMAIL_TEMPLATE_ACTIVATION = Path(
    __file__).parent / "../lib/templates/user-activation.html"

EMAIL_TEMPLATE_RECOVER = Path(
    __file__).parent / "../lib/templates/recover-password.html"

# JWT
###############################
JWT_KEY_PATH = Path(__file__).parent / ".." / config('JWT_KEY_PATH')
JWT_CERT_PATH = Path(__file__).parent / ".." / config('JWT_CERT_PATH')
ACTIVATION_KEY_LENGTH = config('ACTIVATION_KEY_LENGTH', cast=int)

# AUTH
###############################
AUTHENTICATION_BASE_URL = config('AUTHENTICATION_BASE_URL')


# IMAGES AND MEDIA
###############################
ASSETS_PATH = Path(__file__).parent / "../assets"
IMAGES_UPLOAD_PATH = ASSETS_PATH / "images/blog"
