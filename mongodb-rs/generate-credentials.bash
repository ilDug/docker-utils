#! /bin/bash

# Define some colors first
NC='\033[0m' # No Color
RED='\033[1;31m'
GREEN='\033[1;32m'
GREY='\033[1;30m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
AZURE='\033[1;34m'
PURPLE='\033[1;35m'
CYAN='\033[0;36m'


# loop until the user enters the user
while true; do
  echo -e "\n${GREY}enter the ${BLUE}username ${GREY} ${NC} "
  read USER

  # check if the username name is not empty
  if [ -z "$USER" ]
  then
    echo -e "${RED}user name cannot be empty${NC}"
  else
    break
  fi
done


# loop until the user enters the database name
while true; do
  echo -e "\n${GREY}enter the ${BLUE}database${GREY} name${NC} "
  read DB

  # check if the database is not empty
  if [ -z "$DB" ]
  then
    echo -e "${RED}database name cannot be empty${NC}"
  else
    break
  fi
done


#  loop until the user enters the hostname
while true; do
  echo -e "\n${GREY}enter the ${BLUE}hostname:ports ${GREY}(e.g. ${PURPLE}localhost:21017${GREY}, OR replica set: ${PURPLE}mongo1.eurokemical.lan:27017,mongo2.eurokemical.lan:27017,mongo3.eurokemical.lan:27017${GREY})${NC} "
  read HOST

  # check if the hostname is not empty 
    if [ -z "$HOST" ]
    then
        echo -e "${RED}hostname cannot be empty${NC}"
        continue
    fi

    # check if the hostname matches the pattern host:port or host:port,host:port,host:port
    if [[ ! $HOST =~ ^[a-zA-Z0-9.-]+:[0-9]+(,[a-zA-Z0-9.-]+:[0-9]+)*$ ]]
    then
        echo -e "${RED}hostname must have the format host:port ${NC}"
    else
        break
    fi

done

#  store in a boolean variable if the hostname is a replica set, following the pattern
if [[ $HOST =~ ^[a-zA-Z0-9.-]+:[0-9]+,[a-zA-Z0-9.-]+:[0-9]+,[a-zA-Z0-9.-]+:[0-9]+$ ]]
then
  IS_REPLICA_SET=true
else
  IS_REPLICA_SET=false
fi

# generate a password
PW=$(openssl rand -base64 512 | tr -dc 'a-zA-Z0-9' | fold -w 64 | head -n 1 | tr -d '\n')



# generate the connection string, and store in a variable MONGO_CS
if [ "$IS_REPLICA_SET" = true ]
then
  MONGO_CS="mongodb://$USER:$PW@$HOST/$DB?authSource=admin&replicaSet=rs0"
else
  MONGO_CS="mongodb://$USER:$PW@$HOST/$DB?authSource=admin"
fi


# print the connection string
echo -e "\n${GREEN} credenziali generate in ./${USER}_credentials${NC}\n"

# save the credentials in a file
cat << EOF > ./${USER}_credentials
username: 
    $USER

password: 
    $PW

database: 
    $DB

host: 
    $HOST

connection string: 
    $MONGO_CS

commands:
    access_to_shell_cmd:
        ssh mongo1 "docker exec -it mongodb mongosh -u root -p \$(cat /var/mongo/MONGO_ROOT_PW) --authenticationDatabase admin"
    
    create_user_cmd: | 
        use admin

        db.createUser({
            user: "$USER",
            pwd: "$PW",
            roles: [
                { db: "$DB", role: "readWrite" },
                { db: "$DB", role: "dbAdmin" },
            ]
        })

    grant_roles_cmd: |
        db.grantRolesToUser(
            "$USER",
            [
                { db: "$DB", role: "userAdmin" },
                { db: "$DB", role: "dbOwner" }
            ]
        )

    change_pw_cmd: |
        use admin
        db.changeUserPassword("$USER", "$PW")
        db.changeUserPassword("$USER", passwordPrompt())

    authentication_cmd: |
        use $DB
        db.auth("$USER", "$PW")

    drop_user_cmd: |
        use admin
        db.dropUser("$USER")
    
EOF
