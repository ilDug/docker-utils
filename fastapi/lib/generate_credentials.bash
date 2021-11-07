
openssl req -x509 -nodes -days 3650 -newkey rsa:4096 \
    -keyout ./keys/auth.key \
    -out ./certs/auth.crt