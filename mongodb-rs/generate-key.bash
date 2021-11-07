echo "creazione delle variabili di sistema"

echo "MONGO_ROOT_PW=$(openssl rand -base64 21)" > .env
cat .env
echo "password root generata"

echo "......"
echo "generazione della key"
mkdir key backup
openssl rand -base64 756 > key/mongo_key_file
chmod 400 key/mongo_key_file

