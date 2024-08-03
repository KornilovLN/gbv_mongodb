from flask import Flask, jsonify, render_template_string
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
    html_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Data Viewer</title>
        <style>
            #data-container {
                height: 80vh;
                overflow-y: auto;
                white-space: pre-wrap;
                background-color: #f4f4f4;
                padding: 10px;
                border: 1px solid #ccc;
            }
        </style>
        <script>
            // Функция для получения данных с сервера и обновления их на странице
            async function fetchData() {
                try {
                    const response = await fetch('/');
                    const data = await response.json();
                    const dataContainer = document.getElementById('data-container');
                    const newData = document.createElement('div');
                    newData.textContent = JSON.stringify(data, null, 4);
                    dataContainer.appendChild(newData); // Добавление новых данных в конец
                    dataContainer.scrollTop = dataContainer.scrollHeight; // Прокрутка вниз после обновления данных
                } catch (error) {
                    console.error('Error fetching data:', error);
                }
            }

            // Вызов функции для получения данных при загрузке страницы
            fetchData();

            // Установка интервала для автоматического обновления данных каждые 20 секунд
            setInterval(fetchData, 20000); // 20000 миллисекунд = 20 секунд
        </script>
    </head>
    <body>
        <h1>Data from MongoDB</h1>
        <div id="data-container"></div>
    </body>
    </html>
    """

    return render_template_string(html_template)


@app.route('/chart')
def chart():
    html_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Data Chart</title>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <style>
            #chart-container {
                width: 80%;
                height: 80vh;
                margin: auto;
            }
        </style>
        <script>
            let chart;

            // Функция для получения данных с сервера и обновления графика
            async function fetchData() {
                try {
                    const response = await fetch('/');
                    const data = await response.json();
                    const labels = data.map(item => item.x.toFixed(2));
                    const values = data.map(item => item.y.toFixed(2));

                    if (chart) {
                        chart.data.labels = labels;
                        chart.data.datasets[0].data = values;
                        chart.update();
                    } else {
                        const ctx = document.getElementById('myChart').getContext('2d');
                        chart = new Chart(ctx, {
                            type: 'line',
                            data: {
                                labels: labels,
                                datasets: [{
                                    label: 'Y values',
                                    data: values,
                                    borderColor: 'rgba(75, 192, 192, 1)',
                                    borderWidth: 1,
                                    fill: false
                                }]
                            },
                            options: {
                                scales: {
                                    x: {
                                        title: {
                                            display: true,
                                            text: 'X (degrees)'
                                        }
                                    },
                                    y: {
                                        title: {
                                            display: true,
                                            text: 'Y'
                                        }
                                    }
                                }
                            }
                        });
                    }
                } catch (error) {
                    console.error('Error fetching data:', error);
                }
            }

            // Вызов функции для получения данных при загрузке страницы
            fetchData();

            // Установка интервала для автоматического обновления данных каждые 20 секунд
            setInterval(fetchData, 20000); // 20000 миллисекунд = 20 секунд
        </script>
    </head>
    <body>
        <h1>Data Chart from MongoDB</h1>
        <div id="chart-container">
            <canvas id="myChart"></canvas>
        </div>
    </body>
    </html>
    """


    return render_template_string(html_template)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
