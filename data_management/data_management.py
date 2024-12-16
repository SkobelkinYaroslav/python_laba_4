from models import Quote
from quote import quote_fetcher
from database import QuoteManagerDB
from typing import List
class DataManagement:
    cur_quote = Quote("None", "None")  # Статическое поле для хранения текущей цитаты

    @classmethod
    def get_random_quote(cls):
        # Получаем случайную цитату через quote_fetcher
        cls.data = quote_fetcher.RandomQuoteFetcher.get_random_quote()
        if isinstance(cls.data, list) and len(cls.data) > 0:
            quote_text = cls.data[0].get("q", "Цитата недоступна")
            author = cls.data[0].get("a", "Автор неизвестен")
            cls.cur_quote = Quote(quote_text, author)
            return cls.cur_quote
        else:
            # Если данные некорректные, возвращаем объект с дефолтными значениями
            cls.cur_quote = Quote("Некорректный формат данных от API", "Неизвестно")
            return cls.cur_quote
    @classmethod
    def get_cur_quote(cls):
        # Возвращаем текущее значение cur_quote
        return cls.cur_quote
    @classmethod
    def save_quote_to_db(cls):
        """Сохранение цитаты в базу данных."""
        return QuoteManagerDB.QuoteManager.save_quote_to_db(cls.cur_quote)

    @classmethod
    def get_all_quotes(cls) -> List[Quote]:
        """Получение всех цитат из базы данных."""
        return QuoteManagerDB.QuoteManager.get_all_quotes()




