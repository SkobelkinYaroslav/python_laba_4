from abc import ABC, abstractmethod
import random
import logging
from data_management import DataManagement
from models import Quote
from translator import QuoteTranslator

class AbstractBackend(ABC):
    @abstractmethod
    def fetch_and_save_quotes(self) -> None:
        """Загружает цитаты из API и сохраняет в базу данных."""
        pass

    @abstractmethod
    def get_user_data(self, user_id: int) -> dict:
        """Получение данных пользователя."""
        pass

    @abstractmethod
    def get_all_quotes(self) -> list:
        """Получить все цитаты."""
        pass

    @abstractmethod
    def get_random_quote(self, user_id: int) -> Quote:
        """Получить случайную цитату для пользователя."""
        pass

    @abstractmethod
    def add_favorite_quote(self, user_id: int) -> str:
        """Добавить последнюю цитату в избранное."""
        pass

    @abstractmethod
    def get_favorite_quotes(self, user_id: int) -> str:
        """Получить список избранных цитат пользователя."""
        pass

    @abstractmethod
    def translate_quote(self, user_id: int) -> Quote:
        """Перевести последнюю цитату пользователя."""
        pass

