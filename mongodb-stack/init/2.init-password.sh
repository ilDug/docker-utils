# mongorestore -v -u <root> -p <password> --authenticationDatabase admin --nsInclude="blog.posts" --drop --dir=/backup/<serial>/ --dryRun

mongo --eval "db.changeUserPassword('myusername', '$MONGO_USER_PW')" admin