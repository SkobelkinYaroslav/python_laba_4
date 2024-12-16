from data_management.data_management import DataManagement
from translator import QuoteTranslator
from tg_bot import TgBot

class Backend:
    def __init__(self, db_config, bot_token):
        self.translator = QuoteTranslator()
        self.data_manager = DataManagement(db_config)
        self.tg_bot = TgBot(bot_token)

    def start(self):
        self.tg_bot.start_polling()

    def fetch_and_save_quotes(self):
        quotes = self.data_manager.fetch_quotes_from_api()
        for quote in quotes:
            self.data_manager.save_quote_to_db(quote)

    def get_all_quotes(self):
        return self.data_manager.get_all_quotes()

    def add_favorite_quote(self, user_id, quote_id):
        self.data_manager.add_favorite_quote(user_id, quote_id)

    def remove_favorite_quote(self, user_id, quote_id):
        self.data_manager.remove_favorite_quote(user_id, quote_id)

    def get_favorite_quotes(self, user_id):
        return self.data_manager.get_favorite_quotes(user_id)

    def translate_quote(self, quote):
        return self.translator.translate(quote)

    def close(self):
        self.data_manager.close()
        self.tg_bot.stop_polling()

# Пример использования
if __name__ == "__main__":
    db_config = {
        "dbname": "postgres",
        "user": "postgres",
        "password": "db",
        "host": "localhost",
        "port": 5432,
    }
    bot_token = "YOUR_TELEGRAM_BOT_TOKEN"

    backend = Backend(db_config, bot_token)

    try:
        # Запуск бота
        backend.start()

        # Получение и сохранение цитат с API
        backend.fetch_and_save_quotes()

        # Получение всех цитат
        all_quotes = backend.get_all_quotes()
        for quote in all_quotes:
            print(quote)

        # Перевод цитаты
        if all_quotes:
            translated_quote = backend.translate_quote(all_quotes[0])
            print("Переведенная цитата:", translated_quote)

        # Добавление цитаты в избранное
        user_id = 1
        quote_id = 1  # Предположим, что у нас есть цитата с ID 1
        backend.add_favorite_quote(user_id, quote_id)
        print(f"Цитата {quote_id} добавлена в избранное для пользователя {user_id}")

        # Получение избранных цитат пользователя
        favorite_quotes = backend.get_favorite_quotes(user_id)
        print(f"Избранные цитаты пользователя {user_id}:")
        for quote in favorite_quotes:
            print(quote)

        # Удаление цитаты из избранного
        backend.remove_favorite_quote(user_id, quote_id)
        print(f"Цитата {quote_id} удалена из избранного пользователя {user_id}")

    finally:
        backend.close()
