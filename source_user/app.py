from flask import Flask, jsonify, render_template
import pymongo
from bson import json_util, ObjectId
from datetime import datetime

app = Flask(__name__)

def convert_bson_to_json(data):
    if isinstance(data, list):
        return [convert_bson_to_json(item) for item in data]
    elif isinstance(data, dict):
        new_data = {}
        for key, value in data.items():
            if isinstance(value, ObjectId):
                new_data[key] = str(value)
            elif isinstance(value, datetime):
                new_data[key] = value.isoformat()
            elif isinstance(value, dict) or isinstance(value, list):
                new_data[key] = convert_bson_to_json(value)
            else:
                new_data[key] = value
        return new_data
    else:
        return data

def get_data():
    try:
        app.logger.info("Connecting to MongoDB...")
        client = pymongo.MongoClient("mongodb://my_mongo:27017/")
        db = client["mydatabase"]
        collection = db["mycollection"]
        app.logger.info("Fetching data from MongoDB...")
        data = list(collection.find().sort("timestamp"))
        app.logger.info(f"Fetched {len(data)} records from MongoDB.")
        return data
    except Exception as e:
        app.logger.error(f"Error fetching data: {e}")
        raise e  # Raise the exception to be caught in the route handler

@app.route('/')
def index():
    try:
        app.logger.info("Handling request to '/' route...")
        data = get_data()
        app.logger.info("Converting BSON to JSON...")
        json_data = convert_bson_to_json(data)
        app.logger.info("Data converted successfully.")
        return jsonify(json_data)
    except Exception as e:
        app.logger.error(f"Error in index route: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/view')
def view():
    app.logger.info("Rendering view.html")
    return render_template('view.html')

@app.route('/chart')
def chart():
    app.logger.info("Rendering chart.html")
    return render_template('chart.html')

@app.route('/combined')
def combined():
    app.logger.info("Rendering combined.html")
    return render_template('combined.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
