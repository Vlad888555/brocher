import mysql.connector
import random
from mysql.connector import Error
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
@app.route('/data', methods=['POST'])
def receive_data():
    # Получаем данные от клиента
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    try:
        # Подключение
        connection = mysql.connector.connect(
            host='localhost',       
            user='root',            
            password='',
            database='test1'
        )
        if connection.is_connected():
            print("Подключение к MySQL прошло успешно!")
            cursor = connection.cursor()

            cssSelector = data['cssSelector']
            url = data['url']
            textContent = data['textContent']
            print(cssSelector)

            # все что есть в базе
            select_query = "SELECT * FROM user"
            cursor.execute(select_query)
            rows = cursor.fetchall()
            print("Данные из таблицы:")
            for row in rows:
                print(row)
            
            #Гинератор ж№п№
            while True:
                number = random.randint(100000, 999999)
                cursor.execute("SELECT COUNT(*) FROM user WHERE user_id = %s", (number,))
                if cursor.fetchone()[0] == 0:
                    query = """
                            INSERT INTO `user` (`id`, `user_id`, `data`, `flag`, `date_time`, `url`)
                            VALUES (NULL, %s, %s, %s, %s, %s)
                            """
                    values = (
                            f'{number}',
                            f'{cssSelector}',
                            '',
                            '',
                            f'{url}'
                            )
                    cursor.execute(query, values)
                    connection.commit()
                    break
                
                
            cursor.close()
            connection.close()
            print("Соединение с MySQL закрыто.")

    except Error as e:
        print("Ошибка подключения к MySQL:", e)

    
    return jsonify(number), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
