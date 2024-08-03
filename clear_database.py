import pymongo

def clear_database():
    try:
        client = pymongo.MongoClient("mongodb://my_mongo:27017/")
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
