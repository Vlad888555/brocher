import mysql.connector
import random
from mysql.connector import Error
from flask import Flask, request, jsonify
from flask_cors import CORS
import telebot
import time
import schedule
import threading 

# Telegram Bot Token
TELEGRAM_BOT_TOKEN = "7903384627:AAGLIY65QvFC-sH3akRYgNvmTiPupLyseWQ"
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
# Это позор
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

# def check_reminders():
#     try:
#         connection = connect_to_database()
#         cursor = connection.cursor(dictionary=True)
#         query = """
#             SELECT id, id_telegram, message, remind_time, repeat_interval
#             FROM user
#             WHERE remind_time <= NOW() AND status = 'pending'
#         """
#         cursor.execute(query)
#         reminders = cursor.fetchall()

#         for reminder in reminders:
#             # Отправляем сообщение через Telegram
#             bot.send_message(reminder["id_telegram"], f"Напоминание: {reminder['message']}")

#             if reminder["repeat_interval"]:
#                 new_remind_time_query = """
#                     UPDATE reminders
#                     SET remind_time = DATE_ADD(NOW(), INTERVAL %s MINUTE)
#                     WHERE id = %s
#                 """
#                 cursor.execute(new_remind_time_query, (reminder["repeat_interval"], reminder["id"]))
#             else:
#                 # Если напоминание не повторяющееся, обновляем статус
#                 update_query = "UPDATE reminders SET status = 'sent' WHERE id = %s"
#                 cursor.execute(update_query, (reminder["id"],))

#             connection.commit()

#         cursor.close()
#         connection.close()
#     except mysql.connector.Error as e:
#         print(f"Ошибка работы с базой данных: {e}")

# #напоминаний
# def reminder_scheduler():
#     schedule.every(1).minute.do(check_reminders)
#     while True:
#         schedule.run_pending()
#         time.sleep(1)


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
                        VALUES (NULL, %s, %s, %s, %s, %s,%s)
                        """
                values = (
                    f'{number}',
                    f'{cssSelector}',
                    '',
                    '',
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

# Функция для запуска Flask
def run_flask():
    app.run(host='0.0.0.0', port=8000)

# Функция для запуска Telegram-бота
def run_telegram_bot():
    bot.polling(none_stop=True)

if __name__ == '__main__':
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()

    # scheduler_thread = threading.Thread(target=reminder_scheduler)
    # scheduler_thread.daemon = True
    # scheduler_thread.start()

    run_telegram_bot()
