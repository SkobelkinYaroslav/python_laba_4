import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from aiogram import F
from tg_bot.interface_tg_bot import AbstractBackend

class TgBot:
    def __init__(self, token: str, backend: AbstractBackend):
        """
        Инициализация бота Telegram.

        :param token: Токен для доступа к API Telegram.
        :param backend: Экземпляр класса Backend для работы с данными.
        """
        self.bot = Bot(token)
        self.dp = Dispatcher()
        self.backend = backend
        self.__logger = logging.getLogger(__name__)

        # Регистрация обработчиков команд
        self.dp.message.register(self.start_handler, Command("start"))
        self.dp.message.register(self.menu_handler, F.text.in_([
            "Рандомная цитата", "Перевести цитату", "Сохранить текущую цитату", "Список сохраненных цитат"
        ]))

    async def start_handler(self, message: types.Message) -> None:
        """
        Обработчик команды /start.

        :param message: Сообщение от пользователя.
        """
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="Рандомная цитата"),
                    KeyboardButton(text="Перевести цитату"),
                ],
                [
                    KeyboardButton(text="Сохранить текущую цитату"),
                    KeyboardButton(text="Список сохраненных цитат"),
                ],
            ],
            resize_keyboard=True
        )
        await message.reply("Выберите действие:", reply_markup=keyboard)

    async def menu_handler(self, message: types.Message) -> None:
        """
        Обработчик меню выбора действий.

        :param message: Сообщение от пользователя.
        """
        user_id = message.from_user.id  # Получаем уникальный идентификатор пользователя
        text = "Неизвестная команда."

        if message.text == "Рандомная цитата":
            quote = self.backend.get_random_quote(user_id)
            text = str(quote)
            self.__logger.info(f"User {user_id} requested a random quote.")
        elif message.text == "Перевести цитату":
            translation = self.backend.translate_quote(user_id)
            text = str(translation)
            self.__logger.info(f"User {user_id} requested to translate a quote.")
        elif message.text == "Сохранить текущую цитату":
            text = self.backend.add_favorite_quote(user_id)
            self.__logger.info(f"User {user_id} saved a quote.")
        elif message.text == "Список сохраненных цитат":
            text = self.backend.get_favorite_quotes(user_id)
            self.__logger.info(f"User {user_id} requested their favorite quotes.")

        await message.answer(text)

    async def run(self) -> None:
        """
        Запуск бота.
        """
        await self.dp.start_polling(self.bot)
