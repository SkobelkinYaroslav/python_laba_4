import os
from dotenv import load_dotenv
from data_management import DataManagement
from translator import QuoteTranslator
from tg_bot import TgBot
from backend import Backend
import asyncio
import logging
import logging.config
import json

# Загрузка переменных из .env
load_dotenv()

def main():
    db_config = {
        "dbname": "postgres",
        "user": "postgres",
        "password": "db",
        "host": "localhost",
        "port": 5432,
    }

    config = None
    with open('configs/logger_config.json', 'r') as file:
        config = json.load(file)
    logging.config.dictConfig(config)

    # Получение токена из окружения
    API_TOKEN = os.getenv("BOT_API_TOKEN")
    if not API_TOKEN:
        raise ValueError("BOT_API_TOKEN не найден в переменных окружения")

    translator = QuoteTranslator()
    data_manager = DataManagement(db_config)
    backend = Backend(translator, data_manager)
    backend.fetch_and_save_quotes()

    tg_bot = TgBot(API_TOKEN, backend)
    asyncio.run(tg_bot.run())


if __name__ == "__main__":
    main()
