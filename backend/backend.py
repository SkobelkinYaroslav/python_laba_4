import random
import logging
from data_management import DataManagement
from models import Quote
from translator import QuoteTranslator
from tg_bot.interface_tg_bot import AbstractBackend

class Backend(AbstractBackend):
    def __init__(self, translator: QuoteTranslator, data_manager: DataManagement):
        """
        Инициализация Backend.

        :param translator: Экземпляр класса QuoteTranslator для перевода цитат.
        :param data_manager: Экземпляр класса DataManagement для управления данными.
        """
        self.translator = translator
        self.data_manager = data_manager
        self.user_data = {}  # Словарь для хранения данных пользователей
        self.__logger = logging.getLogger(__name__)

    def fetch_and_save_quotes(self) -> None:
        """Загружает цитаты из API и сохраняет в базу данных."""
        quotes = self.data_manager.fetch_quotes_from_api()
        for quote in quotes:
            self.data_manager.save_quote_to_db(quote)
            self.__logger.info(f"Saved quote to database: {quote}")

    def get_user_data(self, user_id: int) -> dict:
        """Получение данных пользователя."""
        if user_id not in self.user_data:
            self.user_data[user_id] = {
                "last_quote": Quote("Последней цитаты нет", "Неизвестно"),
                "favorites": [],
            }
        return self.user_data[user_id]

    def get_all_quotes(self) -> list:
        """Получить все цитаты."""
        return self.data_manager.get_all_quotes()

    def get_random_quote(self, user_id: int) -> Quote:
        """Получить случайную цитату для пользователя."""
        quotes = self.get_all_quotes()
        random_quote = random.choice(quotes)
        self.get_user_data(user_id)["last_quote"] = random_quote
        self.__logger.info(f"User {user_id} received a random quote: {random_quote}")
        return random_quote

    def add_favorite_quote(self, user_id: int) -> str:
        """Добавить последнюю цитату в избранное."""
        user_data = self.get_user_data(user_id)
        last_quote = user_data["last_quote"]
        if last_quote not in user_data["favorites"]:
            user_data["favorites"].append(last_quote)
            self.__logger.info(f"User {user_id} added a quote to favorites: {last_quote}")
            return f"Цитата добавлена в избранное: {last_quote}"
        return "Эта цитата уже в избранном."

    def get_favorite_quotes(self, user_id: int) -> str:
        """Получить список избранных цитат пользователя."""
        favorites = self.get_user_data(user_id)["favorites"]
        if favorites:
            return "\n\n".join(str(quote) for quote in favorites)
        return "У вас нет избранных цитат."

    def translate_quote(self, user_id: int) -> Quote:
        """Перевести последнюю цитату пользователя."""
        last_quote = self.get_user_data(user_id)["last_quote"]
        translated_quote = self.translator.translate(last_quote)
        self.__logger.info(f"User {user_id} translated a quote: {last_quote} -> {translated_quote}")
        return translated_quote