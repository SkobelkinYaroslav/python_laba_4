from laba4.data_management import DataManagement
from laba4.models import Quote
from laba4.translator import QuoteTranslator


class Backend:
    def __init__(self, translator: QuoteTranslator, data_manager: DataManagement):
        self.translator = translator
        self.data_manager = data_manager

    def fetch_and_save_quotes(self):
        quotes = self.data_manager.fetch_quotes_from_api()
        for quote in quotes:
            self.data_manager.save_quote_to_db(quote)

    def get_all_quotes(self):
        return self.data_manager.get_all_quotes()

    def add_favorite_quote(self, user_id: int, quote_id: int):
        self.data_manager.add_favorite_quote(user_id, quote_id)

    def remove_favorite_quote(self, user_id: int, quote_id: int):
        self.data_manager.remove_favorite_quote(user_id, quote_id)

    def get_favorite_quotes(self, user_id: int):
        return self.data_manager.get_favorite_quotes(user_id)

    def translate_quote(self, quote: Quote):
        return self.translator.translate(quote)

    def close(self):
        self.data_manager.close()
