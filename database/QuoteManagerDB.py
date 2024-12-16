import sqlite3
from typing import List
from models import Quote
class QuoteManager:
    @staticmethod
    def save_quote_to_db(quote: Quote, db_path: str = "../quotes.db"):
        """Сохранение цитаты в базу данных."""
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO quotes (text, author)
                VALUES (?, ?)
                """,
                (quote.text, quote.author)
            )
            connection.commit()
            return cursor.lastrowid
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def get_all_quotes(db_path: str = "../quotes.db") -> List[Quote]:
        """Получение всех цитат из базы данных."""
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT id, text, author FROM quotes;")
            rows = cursor.fetchall()
            return [Quote(text=row[1], author=row[2]) for row in rows]
        finally:
            cursor.close()
            connection.close()

# Функция для создания таблиц
def create_tables(db_path: str = "../quotes.db"):
    try:
        # Подключение к базе данных SQLite
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        # Создание таблицы quotes
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS quotes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT NOT NULL,
                author TEXT NOT NULL
            );
            """
        )

        print("Таблицы успешно созданы.")

    except sqlite3.Error as err:
        print(f"Ошибка: {err}")

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

