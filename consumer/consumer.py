import time
import os
import requests

# Получаем URL producer из переменной окружения
PRODUCER_URL = os.getenv('PRODUCER_URL', 'http://producer:5000')


def get_data_from_producer():
    """Делает GET-запрос к producer и возвращает ответ"""
    try:
        response = requests.get(f"{PRODUCER_URL}/data", timeout=5)
        if response.status_code == 200:
            return response.text
        else:
            return f"Error: Producer returned status {response.status_code}"
    except requests.exceptions.ConnectionError:
        return "Error: Cannot connect to producer"
    except requests.exceptions.Timeout:
        return "Error: Request timeout"
    except Exception as e:
        return f"Error: {str(e)}"


def main():
    """Основной цикл consumer"""
    print("Consumer запущен")
    print(f"Пытаюсь подключиться к producer по адресу: {PRODUCER_URL}")

    # Счётчик попыток для отображения
    attempt = 1

    while True:
        print(f"\n--- Попытка {attempt} ---")
        print(f"Запрос к {PRODUCER_URL}/data")

        # Получаем данные от producer
        data = get_data_from_producer()

        # Выводим полученные данные
        print(f"Получено: {data}")

        # Ждём 5 секунд перед следующим запросом
        time.sleep(5)
        attempt += 1


if __name__ == '__main__':
    main()