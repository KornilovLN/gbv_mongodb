# datauser/data_user.py

import os
import pymongo
import time
import json
from bson import json_util

#MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://my_mongo:27017/')
MONGO_URI = os.environ.get('MONGO_URI')
PAUSE_TIME = int(os.environ.get('PAUSE_TIME', 5))

def fetch_data():
    while True:
        try:
            #client = pymongo.MongoClient("mongodb://my_mongo:27017/")
            client = pymongo.MongoClient(MONGO_URI)
            db = client["mydatabase"]
            collection = db["mycollection"]

            while True:
                #records = list(collection.find().sort("timestamp", -1).limit(MAX_RECORDS))
                for record in collection.find().sort("timestamp"):
                #for record in reversed(records):    
                    record["x"] = float(record["x"])
                    record["y"] = float(record["y"]) 
                    print(json.dumps(record, indent=4, default=json_util.default))               
                time.sleep(PAUSE_TIME)

        except pymongo.errors.ServerSelectionTimeoutError as err:
            print("Could not connect to MongoDB: ", err)
            time.sleep(PAUSE_TIME)

if __name__ == "__main__":
    time.sleep(10)  # Wait for MongoDB to be ready
    fetch_data()

