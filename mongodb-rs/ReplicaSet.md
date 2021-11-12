# Replica Set

Creare la chiave di interconnessione ai container
```
bash generate-key.bash
```

Avviare tutti i container e tutti i Docker.

Nel PRIMARY entrare ed eseguir i comandi per configurare il replica Set.

```
docker exec -it mongodb bash
```

una volta dentro il container,  aprire la shell di mongo ed eseguire le seguenti impostazioni:

```javascript
rsconf = {
    _id: "rs0",
    members: [
        {
            "_id": 0,
            "host": "mongo1.dag.lan:27017",
            "priority": 1
        },
        {
            "_id": 1,
            "host": "mongo2.dag.lan:27017",
            "priority": 1
        },
        {
            "_id": 2,
            "host": "mongo3.dag.lan:27017",
            "priority": 1
        }
    ]
}


rs.initiate(rsconf)
rs.conf()
rs.status()
```

Creare l'utente ROOT solo nel primo:

```javascript
admin = db.getSiblingDB("admin")
admin.createUser(
    {
        user: "root",
        pwd: "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
        roles: [
            { db: "admin", role: "userAdminAnyDatabase"},
            { db: "admin", role: "dbAdminAnyDatabase" },
            { db: "admin", role: "clusterAdmin" },
            { db: "admin", role: "root" },
        ]
    }
)

db.grantRolesToUser("root", [
    { db: "admin", role: "userAdminAnyDatabase"},
    { db: "admin", role: "dbAdminAnyDatabase" },
    { db: "admin", role: "clusterAdmin" },
    { db: "admin", role: "root" },

])

rs.conf()
rs.status()
```

In un container SECONDARY abilitare la lettura dagli altri nodi sempre dalla shell di mongo :

```
rs.secondaryOk() 
```

# Connection String

```
mongodb://root:xxxxxxx@mongo1.dag.lan:27017,mongo2.dag.lan:27017,mongo3.dag.lan:27017/?replicaSet=rs0
```

```
mongodb://username:XXXXXXXXXXX@mongo1.dag.lan:27017,mongo2.dag.lan:27017,mongo3.dag.lan:27017/databasename?authSource=admin&replicaSet=rs0
```


# Add Users


```javascript
use admin
db.createUser({ 
    user: "ekuser" , 
    pwd: "xxxxxxxx", 
    roles: [
        { db: "ek", role: "readWrite" },
        { db: "ek", role: "dbOwner" },
    ]
})


db.changeUserPassword("ekuser", passwordPrompt())


```
