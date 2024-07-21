# datagenerator/data_generator.py

import pymongo
import time
from datetime import datetime
import random

def generate_data():
    client = pymongo.MongoClient("mongodb://mongo_gen:27017/")
    db = client["mydatabase"]
    collection = db["mycollection"]
    while True:
        x_value = random.randint(1, 100)
        y_value = x_value * 2  # Example computation
        data = {
            "x": x_value,
            "y": y_value,
            "timestamp": datetime.utcnow()
        }
        collection.insert_one(data)
        print(f"Inserted data: {data}")
        time.sleep(5)

if __name__ == "__main__":
    time.sleep(10)  # Wait for MongoDB to be ready
    generate_data()
