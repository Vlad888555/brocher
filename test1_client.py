import requests

def send_data_to_server(data):
    url = 'http://127.0.0.1:5000/data'  # URL сервера
    try:
        # Отправляем POST-запрос с данными
        response = requests.post(url, json=data)
        if response.status_code == 200:
            print("Ответ от сервера:", response.json())
        else:
            print("Ошибка:", response.status_code, response.text)
    except requests.exceptions.RequestException as e:
        print("Ошибка подключения к серверу:", e)

if __name__ == '__main__':
    # Пример данных для отправки
    sample_data = {
        'name': 'John Doe',
        'age': 30,
        'message': 'Hello from the client!'
    }
    send_data_to_server(sample_data)
