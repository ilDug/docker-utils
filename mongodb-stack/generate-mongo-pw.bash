echo "creazione delle variabili di sistema"
echo "MONGO_ROOT_PW=$(openssl rand -base64 21)" > .env
cat .env
echo "password root generata"
