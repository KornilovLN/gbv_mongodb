# datagenerator/data_generator.py

import pymongo
from bson.objectid import ObjectId
import time
from datetime import datetime
import math
import random
import os


#MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://mongo_gen:27017/')
MONGO_URI = os.environ.get('MONGO_URI')
MAX_RECORDS = int(os.environ.get('MAX_RECORDS', 512))
PAUSE_TIME = int(os.environ.get('PAUSE_TIME', 5))

def generate_data():
    #client = pymongo.MongoClient("mongodb://mongo_gen:27017/")
    client = pymongo.MongoClient(MONGO_URI)
    db = client["mydatabase"]
    collection = db["mycollection"]

    x_value = 0.0
    delta_x = 5 * math.pi / 180  # Шаг приращения

    record_count = 0

    while True:
        
        # Генерация случайных данных        
        y_rnd = random.uniform(-25.0, 25.0) 
        k_rnd = random.uniform(1.0, 5.0)
        
        # Вычисление значений x и y с примесью шума
        x_value += delta_x
        y_value = 1000 * math.sin(x_value) + y_rnd * k_rnd

        # Получение статистики базы данных
        stats = db.command("dbstats")

        data = {
            "x": x_value,
            "y": y_value,
            "timestamp": ObjectId().generation_time,
            "db_stats": {
                "storageSize": stats["storageSize"],
                "timestamp": datetime.now()
            }
        }
        collection.insert_one(data)

        
        record_count += 1
        if record_count >= MAX_RECORDS: # Clear the entire collection
            collection.delete_many({})
            record_count = 0
            print("Table cleared after reaching {MAX_RECORDS} records")
        
    
        '''
        if record_count > MAX_RECORDS:
            oldest_record = collection.find_one(sort=[("timestamp", 1)])
            if oldest_record:
                collection.delete_one({"_id": oldest_record["_id"]})
        '''

        print(f"Inserted data: {data}")


        time.sleep(PAUSE_TIME)

if __name__ == "__main__":
    time.sleep(10)  # Wait for MongoDB to be ready
    generate_data()
