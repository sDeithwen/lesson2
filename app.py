import sys
import time
from loguru import logger

LOG_MESSAGE = "Контейнер запущен и работает"
SLEEP_SECONDS = 5

logger.remove()
logger.add(
    sys.stdout,
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"
)

def main():
    logger.info("Приложение стартовало")

    while True:
        logger.info(LOG_MESSAGE)
        time.sleep(SLEEP_SECONDS)

if __name__ == "__main__":
    main()
