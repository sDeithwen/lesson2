import time
import os
from flask import Flask, Response
import threading

app = Flask(__name__)

DATA_FILE = '/data/data.txt'
is_ready = False


def read_data():
    """Читает содержимое файла /data/data.txt"""
    try:
        with open(DATA_FILE, 'r') as f:
            content = f.read()
            return content if content else ""
    except FileNotFoundError:
        return "File not found"
    except Exception as e:
        return f"Error: {str(e)}"


def background_reader():
    """Фоновый поток для периодического вывода содержимого файла в консоль"""
    global is_ready

    print("Запускаемся, ожидайте 5 секунд...", flush=True)
    time.sleep(5)

    is_ready = True
    print("Сервис запущен, начинаем мониторинг файла", flush=True)

    greeting = os.getenv('GREETING', 'Default greeting')

    while True:
        content = read_data()
        if content == "":
            print(f"Файл: (пустой), Env: {greeting}", flush=True)
        else:
            print(f"Файл: {content}, Env: {greeting}", flush=True)
        time.sleep(5)


@app.route('/health')
def health():
    global is_ready
    if is_ready:
        return "OK", 200
    else:
        return "Service not ready yet", 503


@app.route('/data')
def get_data():
    global is_ready

    if not is_ready:
        return "Service not ready yet", 503

    file_content = read_data()
    greeting = os.getenv('GREETING', 'Default greeting')

    if file_content == "":
        result = f"File: (empty), Env: {greeting}"
    else:
        result = f"File: {file_content}, Env: {greeting}"

    return Response(result, mimetype='text/plain')


if __name__ == '__main__':
    reader_thread = threading.Thread(target=background_reader, daemon=True)
    reader_thread.start()

    # Отключаем буферизацию stdout
    os.environ['PYTHONUNBUFFERED'] = '1'

    app.run(host='0.0.0.0', port=5000, debug=False)