admin = db.getSiblingDB("admin")

admin.createUser({
    user: "myusername",
    pwd: "xxxxxxxx",
    roles: [
        { db: "mydb", role: "readWrite" },
        { db: "mydb", role: "dbOwner" },
    ]
})

db.changeUserPassword("myusername", "xxxxxxxx")


mydb = db.getSiblingDB('mydb')
coll1 = users.createCollection("mycollection1")
coll2 = users.createCollection("mycollection2")