import requests
import psycopg2
from psycopg2 import sql
from ..models import Quote


class DataManagement:
    def __init__(self, db_config):
        """
        Инициализация модуля работы с данными.
        :param db_config: словарь с конфигурацией подключения к базе данных
        """
        self.connection = psycopg2.connect(**db_config)
        self.cursor = self.connection.cursor()
        self._create_tables()

    def _create_tables(self):
        """Создание таблиц, если они не существуют."""
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS quotes (
                id SERIAL PRIMARY KEY,
                text TEXT NOT NULL,
                author TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS favorite_quotes (
                id SERIAL PRIMARY KEY,
                user_id BIGINT NOT NULL,
                quote_id INT NOT NULL REFERENCES quotes(id) ON DELETE CASCADE
            );
            """
        )
        self.connection.commit()

    def fetch_quotes_from_api(self):
        """Получение данных с API и возврат списка цитат."""
        url = "https://zenquotes.io/api/quotes"
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception(f"Ошибка при получении данных с API: {response.status_code}")

        quotes_data = response.json()
        quotes = [
            Quote(text=quote["q"], author=quote["a"])
            for quote in quotes_data
        ]
        return quotes

    def save_quote_to_db(self, quote: Quote):
        """Сохранение цитаты в базу данных."""
        self.cursor.execute(
            """
            INSERT INTO quotes (text, author)
            VALUES (%s, %s)
            RETURNING id;
            """,
            (quote.text, quote.author),
        )
        quote_id = self.cursor.fetchone()[0]
        self.connection.commit()
        return quote_id

    def get_all_quotes(self):
        """Получение всех цитат из базы данных."""
        self.cursor.execute("SELECT id, text, author FROM quotes;")
        rows = self.cursor.fetchall()
        return [Quote(text=row[1], author=row[2]) for row in rows]

    def add_favorite_quote(self, user_id: int, quote_id: int):
        """Добавление цитаты в избранное пользователя."""
        self.cursor.execute(
            """
            INSERT INTO favorite_quotes (user_id, quote_id)
            VALUES (%s, %s);
            """,
            (user_id, quote_id),
        )
        self.connection.commit()

    def remove_favorite_quote(self, user_id: int, quote_id: int):
        """Удаление цитаты из избранного пользователя."""
        self.cursor.execute(
            """
            DELETE FROM favorite_quotes
            WHERE user_id = %s AND quote_id = %s;
            """,
            (user_id, quote_id),
        )
        self.connection.commit()

    def get_favorite_quotes(self, user_id: int):
        """Получение всех избранных цитат пользователя."""
        self.cursor.execute(
            """
            SELECT q.text, q.author
            FROM favorite_quotes fq
            JOIN quotes q ON fq.quote_id = q.id
            WHERE fq.user_id = %s;
            """,
            (user_id,),
        )
        rows = self.cursor.fetchall()
        return [Quote(text=row[0], author=row[1]) for row in rows]

    def close(self):
        """Закрытие соединения с базой данных."""
        self.cursor.close()
        self.connection.close()


# # Пример использования
# if __name__ == "__main__":
#     db_config = {
#         "dbname": "postgres",
#         "user": "postgres",
#         "password": "db",
#         "host": "localhost",
#         "port": 5432,
#     }
#
#     data_manager = DataManagement(db_config)
#
#     try:
#         # Получение цитат с API
#         quotes = data_manager.fetch_quotes_from_api()
#         print("Получено цитат с API:", len(quotes))
#
#         # Сохранение первой цитаты в базу данных
#         if quotes:
#             quote_id = data_manager.save_quote_to_db(quotes[0])
#             print("Сохранена цитата с ID:", quote_id)
#
#         # Получение всех цитат
#         all_quotes = data_manager.get_all_quotes()
#         for quote in all_quotes:
#             print(quote)
#
#         # Добавление цитаты в избранное
#         user_id = 1
#         data_manager.add_favorite_quote(user_id, quote_id)
#         print(f"Цитата {quote_id} добавлена в избранное для пользователя {user_id}")
#
#         # Получение избранных цитат пользователя
#         favorite_quotes = data_manager.get_favorite_quotes(user_id)
#         print(f"Избранные цитаты пользователя {user_id}:")
#         for quote in favorite_quotes:
#             print(quote)
#
#         # Удаление цитаты из избранного
#         data_manager.remove_favorite_quote(user_id, quote_id)
#         print(f"Цитата {quote_id} удалена из избранного пользователя {user_id}")
#
#     finally:
#         data_manager.close()
