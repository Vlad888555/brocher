from flask import Flask, request, jsonify
import mysql.connector
import requests
from bs4 import BeautifulSoup
import schedule
import time
import threading

app = Flask(__name__)

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="parser_db"
    )

@app.route('/data', methods=['POST'])
def receive_data():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Нет данных'}), 400

    try:
        connection = connect_db()
        cursor = connection.cursor()
        query = """
            INSERT INTO elements (url, css_selector, user_id, status)
            VALUES (%s, %s, %s, %s)
        """
        values = (data['url'], data['cssSelector'], None, 1)
        cursor.execute(query, values)
        connection.commit()
        return jsonify({'id': cursor.lastrowid}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def parse_website():
    connection = connect_db()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM elements WHERE status = 1")
    elements = cursor.fetchall()

    for element in elements:
        try:
            response = requests.get(element["url"])
            soup = BeautifulSoup(response.text, "html.parser")
            data = soup.select_one(element["css_selector"])
            result = data.text.strip() if data else 'Элемент не найден'
            print(f"Парсинг {element['url']}: {result}")
        except Exception as e:
            print(f"Ошибка парсинга: {e}")

def run_scheduler():
    schedule.every(1).minutes.do(parse_website)
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    # Запуск планировщика в отдельном потоке
    scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()

    # Запуск Flask-сервера
    app.run(host="0.0.0.0", port=8000, debug=True)
