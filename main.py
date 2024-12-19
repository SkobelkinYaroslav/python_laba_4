from laba4.data_management import DataManagement
from laba4.translator import QuoteTranslator
from tg_bot import TgBot
from backend import Backend
import asyncio

# TODO: УБЕРИ ХУЙНЮ ЭТУ
API_TOKEN = '8098328078:AAHA6uAduMhR-4FSsWZJIY-awG7FKKL-fAM'


def main():
    db_config = {
        "dbname": "postgres",
        "user": "postgres",
        "password": "db",
        "host": "localhost",
        "port": 5432,
    }

    translator = QuoteTranslator()
    data_manager = DataManagement(db_config)
    backend = Backend(translator, data_manager)
    backend.fetch_and_save_quotes()

    tg_bot = TgBot(API_TOKEN, backend)
    asyncio.run(tg_bot.run())


if __name__ == "__main__":
    main()
