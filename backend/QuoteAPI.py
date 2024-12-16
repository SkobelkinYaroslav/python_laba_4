from data_management import DataManagement
from translator import QuoteTranslator
from models import Quote
from flask import Flask, jsonify
from flask_cors import CORS

class BackendAPI:
    def __init__(self, app: Flask):
        self.app = app
        CORS(self.app)  # Если вы хотите поддерживать CORS на всех маршрутах

        # Регистрация маршрутов
        self.app.add_url_rule('/api/random_quote', 'get_new_quote', self.get_new_quote, methods=['GET'])
        self.app.add_url_rule('/api/best_quotes', 'get_best_quotes', self.get_best_quotes, methods=['GET'])
        self.app.add_url_rule('/api/translate', 'translate_current_quote', self.translate_current_quote, methods=['GET'])
        self.app.add_url_rule('/api/save_quote', 'save_quote', self.save_quote, methods=['POST'])
        self.app.add_url_rule('/api/get_all_quotes', 'get_all_quotes', self.get_all_quotes, methods=['GET'])
    def get_new_quote(self):
        # Возвращаем случайную цитату через DataManagement
        quote = DataManagement.get_random_quote()
        # Используем jsonify для автоматической сериализации в JSON и установки правильного заголовка
        return jsonify(quote.__dict__)

    def get_best_quotes(self):
        # Пример вывода списка лучших цитат
        print("*List of best quotes*")
        # Здесь логика для получения лучших цитат, например:
        # best_quotes = DataManagement.get_best_quotes()
        # return jsonify(best_quotes), 200
        return jsonify({"message": "Best quotes logic not implemented yet"}), 200

    def translate_current_quote(self):
        # Перевод текущей цитаты с помощью QuoteTranslator
        quote = DataManagement.get_cur_quote()
        translated_quote = QuoteTranslator.translate(quote)
        # Используем jsonify для корректной сериализации
        return jsonify(translated_quote.__dict__)


    def save_quote(self):
        DataManagement.save_quote_to_db()
        return "", 200
    def get_all_quotes(self):
        quotes_list = DataManagement.get_all_quotes()
        return jsonify([quote.__dict__ for quote in quotes_list])

