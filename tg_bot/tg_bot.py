from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.filters import Command
from aiogram import F
import asyncio
from laba4.backend.backend import Backend  # Импортируем ваш класс Backend

API_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'  # Замените на токен вашего бота

class TgBot:
    def __init__(self, token: str, backend: Backend):
        self.bot = Bot(token)
        self.dp = Dispatcher()  # Создаем диспетчер
        self.backend = backend

        # Регистрация обработчиков команд
        self.dp.message.register(self.start_handler, Command("start"))
        self.dp.message.register(self.menu_handler, F.text.in_([
            "Рандомная цитата", "Перевести цитату", "Сохранить текущую цитату", "Список сохраненных цитат"
        ]))

    async def start_handler(self, message: types.Message):
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
            resize_keyboard=True,
            one_time_keyboard=True  # Если нужно, чтобы клавиатура исчезала после нажатия
        )

        await message.reply("Выберите действие:", reply_markup=keyboard)

    async def menu_handler(self, message: types.Message):
        if message.text == "Рандомная цитата":
            print("RANDOM QUOTE HIT")
            text = self.backend.get_all_quotes()  # TODO: поебень
        elif message.text == "Перевести цитату":
            text = self.backend.translate_quote()  # Вызов метода бэкенда
        elif message.text == "Сохранить текущую цитату":
            text = self.backend.add_favorite_quote()  # Вызов метода бэкенда
        elif message.text == "Список сохраненных цитат":
            text = self.backend.get_all_quotes()  # Вызов метода бэкенда
        else:
            text = "Неизвестная команда."

        await message.answer(text)
        await asyncio.sleep(5)
        await self.bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)

    async def run(self):
        await self.dp.start_polling(self.bot)

# Пример использования
if __name__ == '__main__':
    backend = Backend()  # Инициализация вашего бэкенда
    bot = TgBot(API_TOKEN, backend)
    asyncio.run(bot.run())
