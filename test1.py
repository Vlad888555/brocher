import mysql.connector
import random
from mysql.connector import Error
from flask import Flask, request, jsonify
from flask_cors import CORS
import telebot
import time
import schedule
import threading
import requests
from bs4 import BeautifulSoup
import chardet

# Telegram Bot Token
TELEGRAM_BOT_TOKEN = "7903384627:AAGLIY65QvFC-sH3akRYgNvmTiPupLyseWQ"
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# Flask-приложение
app = Flask(__name__)
CORS(app)

# Подключение к базе данных
def connect_to_database():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="test1"
    )
    
def parse_data(url, css_selector):
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        detected_encoding = chardet.detect(response.content)['encoding']
        response.encoding = detected_encoding

        soup = BeautifulSoup(response.text, 'html.parser')
        element = soup.select_one(css_selector)
        return element.text.strip() if element else f"Элемент '{css_selector}' не найден."
    except requests.exceptions.RequestException as e:
        return f"Ошибка HTTP-запроса: {e}"
    except Exception as e:
        return f"Ошибка парсинга: {e}"
    
        
def check_reminders():
    
    try:
        connection = connect_to_database()
        cursor = connection.cursor(dictionary=True)
        query = """
            SELECT id, date_time, status, data, id_telegram, url
            FROM user
            WHERE date_time <= NOW() AND status = '1'
        """
        cursor.execute(query)
        reminders = cursor.fetchall()

        for reminder in reminders:
            chat_id = reminder["id_telegram"]
            message_text = f"Напоминание: {reminder['data']}"
            
            if chat_id != 0:
                try:
                    chat_id = int(chat_id)
                    message = parse_data(reminder['url'], reminder['data'])
                    bot.send_message(chat_id, message.encode('utf-8').decode('utf-8'))
                    print(f"Сообщение успешно отправлено: {chat_id}")


                    update_query = """
                        UPDATE user
                        SET date_time = DATE_ADD(NOW(), INTERVAL 5 MINUTE)
                        WHERE id = %s
                    """
                    cursor.execute(update_query, (reminder["id"],))
                    connection.commit()
                except telebot.apihelper.ApiTelegramException as e:
                    print(f"Ошибка Telegram API (id: {chat_id}): {e}")
                except Exception as e:
                    print(f"Другая ошибка (id: {chat_id}): {e}")
            else:
                print(f"Пропущено: id_telegram пустой (id: {reminder['id']})")
                

        cursor.close()
        connection.close()
    except mysql.connector.Error as e:
        print(f"Ошибка работы с базой данных: {e}")


#напоминаний
def reminder_scheduler():
    schedule.every(1).minute.do(check_reminders)
    while True:
        schedule.run_pending()
        time.sleep(1)


#бот телеграм
@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я бот-парсер. Чтоб начать просто вставте id от расширения")
    bot.register_next_step_handler(message, reg_user)

def reg_user(message):
    id = message.text.strip()
    connection = connect_to_database()
    cursor = connection.cursor()
    tl_id = message.from_user.id
    update = f"UPDATE `user` SET `id_telegram` = {tl_id} WHERE `user`.`user_id` = {id};"
    cursor.execute(update)
    connection.commit()
    bot.reply_to(message, f"{tl_id} || {id}")
    
    

#сервер
@app.route('/data', methods=['POST'])
def receive_data():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    try:
        connection = connect_to_database()
        cursor = connection.cursor()

        cssSelector = data['cssSelector']
        url = data['url']
        textContent = data['textContent']

            
        while True:
            number = random.randint(100000, 999999)
            cursor.execute("SELECT COUNT(*) FROM user WHERE user_id = %s", (number,))
            if cursor.fetchone()[0] == 0:
                query = """
                        INSERT INTO `user` (`id`, `user_id`, `data`, `status`, `date_time`, `url`, `id_telegram`)
                        VALUES (NULL, %s, %s, %s, NOW(), %s,%s)
                        """
                values = (
                        f'{number}',
                        f'{cssSelector}',
                        '1',
                        #date_time
                        f'{url}',
                        ''
                    )
                cursor.execute(query, values)
                connection.commit()
                break
            
    except Error as e:
        print("Ошибка подключения к MySQL:", e)
        return jsonify({'error': str(e)}), 500

    return jsonify(number), 200

# колаба
@app.route("/new")
def new_pars():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    url = data["url"]
    cssSelector = data["data"]
    id_case = data["id_case"]
    try:
        connect = connect_to_database()
        cursor = connect.cursor()
        query = """
                INSERT INTO `colaget` (`id`, `data`, `url`, `data_time`, `id_case`)
                VALUES (NULL, '%s', '%s', '%s', '%s')
                """
        values = (
            f'{cssSelector}',
            f'{url}',
            f'',
            f'{id_case}',
        )
        cursor.execute(query, values)
        connect.commit()
    except Error as e:
        print("ошыбка га сервй ", e)
        return jsonify({'error': '000000'}), 500
    return jsonify("все ок"), 200

    
@app.route("/get")
def get_element():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    id_case = data["id_case"]
    
    try:
        connect = connect_to_database()
        cursor = connect.cursor()
        query = """
                SELECT * FROM colaget WHERE id_case = %s
                """
        values = (
            f'{id_case}',
        )
        cursor.execute(query, values)
        connect.commit()
        
    except Error as e:
        print("ошыбка га сервй ", e)
        return jsonify({'error': '000000'}), 500
    return jsonify("все ок"), 200
    


def run_flask():
    app.run(host='0.0.0.0', port=8000)


def run_telegram_bot():
    bot.polling(none_stop=True)

if __name__ == '__main__':
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()

    scheduler_thread = threading.Thread(target=reminder_scheduler)
    scheduler_thread.daemon = True
    scheduler_thread.start()

    run_telegram_bot()
