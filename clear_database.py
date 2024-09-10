#!/usr/bin/env python3

import pymongo

def clear_database():
    try:
        #--- Находим IP адрес контейнера с MongoDB
        #--- docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' my_mongo
        #--- 172.21.0.2 или 172.20.0.2 было найдено в
        #--- docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' my_mongo
#       --- После этого запускаем скрипт вставив найденный IP адрес в строку ниже

        client = pymongo.MongoClient("mongodb://172.21.0.2:27017/")
        db = client["mydatabase"]
        collection = db["mycollection"]
        
        # Удаление всех документов из коллекции
        result = collection.delete_many({})
        print(f"Deleted {result.deleted_count} documents from the collection.")
        
        # Если нужно удалить саму коллекцию, используйте:
        # db.drop_collection("mycollection")
        # print("Collection dropped.")
        
    except pymongo.errors.ServerSelectionTimeoutError as err:
        print("Could not connect to MongoDB: ", err)

if __name__ == "__main__":
    clear_database()

'''
Можно вручную удалить все данные из коллекции, используя:

1. Выполнить команду в контейнере MongoDB:
$ docker exec -it my_mongo mongosh

Current Mongosh Log ID: 66de084a20037b99445e739b
Connecting to:          mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+2.3.0
Using MongoDB:          7.0.14
Using Mongosh:          2.3.0

For mongosh info see: https://www.mongodb.com/docs/mongodb-shell/

------
   The server generated these startup warnings when booting
   2024-09-08T20:09:17.826+00:00: Using the XFS filesystem is strongly recommended with the WiredTiger storage engine. See http://dochub.mongodb.org/core/prodnotes-filesystem
   2024-09-08T20:09:19.458+00:00: Access control is not enabled for the database. Read and write access to data and configuration is unrestricted
   2024-09-08T20:09:19.458+00:00: vm.max_map_count is too low
------

2. Выполнить команду в MongoDB поиска зарегистрированных баз данных:
test> use mydatabase
switched to db mydatabase

3. Выполнить команду в MongoDB поиска зарегистрированных коллекций:
test> show collections
mycollection

4. Выполнить команду в MongoDB удаления найденной коллекции:
test> db.mycollection.deleteMany({})
{ acknowledged: true, deletedCount: 12065 }

mydatabase> exit
'''