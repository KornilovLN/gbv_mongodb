# datagenerator/data_generator.py

import pymongo
from bson.objectid import ObjectId
import time
from datetime import datetime
import math
import random

def generate_data():
    client = pymongo.MongoClient("mongodb://mongo_gen:27017/")
    db = client["mydatabase"]
    collection = db["mycollection"]

    x_value = 0.0
    delta_x = 5 * math.pi / 180  # Шаг приращения в радианах

    while True:
        '''
        # Генерация случайных данных        
        x_value = random.randint(1, 100)
        y_value = x_value * 2  # Example computation
        '''
        
        # Вычисление значений x и y
        x_value += delta_x
        y_value = 1000 * math.sin(x_value)

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
        print(f"Inserted data: {data}")


        time.sleep(5)

if __name__ == "__main__":
    time.sleep(10)  # Wait for MongoDB to be ready
    generate_data()
