import requests
import psycopg2
from models import Quote
import logging
from typing import List, Dict


class DataManagement:
    def __init__(self, db_config: Dict[str, str]):
        """
        Инициализация модуля управления данными.

        :param db_config: Словарь с конфигурацией подключения к базе данных.
        """
        self.__logger = logging.getLogger(__name__)
        self.__logger.debug("Initializing DataManagement")
        self.connection = psycopg2.connect(**db_config)
        self.cursor = self.connection.cursor()
        self._create_tables()

    def _create_tables(self) -> None:
        """Создание таблиц в базе данных, если они не существуют."""
        self.__logger.info("Creating database tables if they do not exist")
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

    def fetch_quotes_from_api(self) -> List[Quote]:
        """
        Получение цитат из внешнего API.

        :return: Список объектов Quote.
        """
        url = "https://zenquotes.io/api/quotes"
        self.__logger.info("Fetching quotes from API")
        response = requests.get(url)
        if response.status_code != 200:
            self.__logger.error(f"API request failed with status code: {response.status_code}")
            raise Exception(f"Error fetching data from API: {response.status_code}")

        quotes_data = response.json()
        quotes = [Quote(text=quote["q"], author=quote["a"]) for quote in quotes_data]
        self.__logger.debug(f"Fetched {len(quotes)} quotes from API")
        return quotes

    def save_quote_to_db(self, quote: Quote) -> int:
        """
        Сохранение цитаты в базе данных.

        :param quote: Объект Quote.
        :return: ID сохраненной цитаты.
        """
        self.__logger.debug(f"Saving quote to DB: {quote}")
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
        self.__logger.info(f"Quote saved to DB with ID: {quote_id}")
        return quote_id

    def get_all_quotes(self) -> List[Quote]:
        """Получение всех цитат из базы данных."""
        self.__logger.debug("Fetching all quotes from DB")
        self.cursor.execute("SELECT id, text, author FROM quotes;")
        rows = self.cursor.fetchall()
        return [Quote(text=row[1], author=row[2]) for row in rows]

    def add_favorite_quote(self, user_id: int, quote_id: int) -> None:
        """
        Добавление цитаты в избранное пользователя.

        :param user_id: ID пользователя.
        :param quote_id: ID цитаты.
        """
        self.__logger.debug(f"Adding favorite quote (User ID: {user_id}, Quote ID: {quote_id})")
        self.cursor.execute(
            """
            INSERT INTO favorite_quotes (user_id, quote_id)
            VALUES (%s, %s);
            """,
            (user_id, quote_id),
        )
        self.connection.commit()

    def remove_favorite_quote(self, user_id: int, quote_id: int) -> None:
        """
        Удаление цитаты из избранного пользователя.

        :param user_id: ID пользователя.
        :param quote_id: ID цитаты.
        """
        self.__logger.debug(f"Removing favorite quote (User ID: {user_id}, Quote ID: {quote_id})")
        self.cursor.execute(
            """
            DELETE FROM favorite_quotes
            WHERE user_id = %s AND quote_id = %s;
            """,
            (user_id, quote_id),
        )
        self.connection.commit()

    def get_favorite_quotes(self, user_id: int) -> List[Quote]:
        """
        Получение всех избранных цитат пользователя.

        :param user_id: ID пользователя.
        :return: Список объектов Quote.
        """
        self.__logger.debug(f"Fetching favorite quotes for User ID: {user_id}")
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

    def close(self) -> None:
        """Закрытие соединения с базой данных."""
        self.__logger.info("Closing database connection")
        self.cursor.close()
        self.connection.close()

