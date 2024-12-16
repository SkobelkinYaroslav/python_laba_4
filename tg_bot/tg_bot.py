from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor
import aiohttp
import asyncio


API_TOKEN = '8098328078:AAHA6uAduMhR-4FSsWZJIY-awG7FKKL-fAM'
BACKEND_URL = 'http://127.0.0.1:5000/api'  # Замените на URL вашего бэкенда

# Создаем бота и диспетчер
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Функция для получения текста с бэкенда
async def get_text_from_backend(endpoint):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{BACKEND_URL}/{endpoint}") as response:
            if response.status == 200:
                data = await response.json()
                return "".join([data.get("_text", "Нет цитаты"), "\n", data.get("_author", "Нет автора")])
            else:
                return "Ошибка при получении данных"

# Функция для получения текста с бэкенда
async def get_all_text_from_backend(endpoint):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{BACKEND_URL}/{endpoint}") as response:
            if response.status == 200:
                data = await response.json()
                
                # Проверяем, является ли data списком
                if isinstance(data, list):
                    # Обрабатываем список и извлекаем _text и _author для каждого элемента
                    readable_text = ""
                    for item in data:
                        # Проверяем, что item является объектом (например, словарем)
                        if isinstance(item, dict):
                            text = item.get('_text', 'Нет текста')
                            author = item.get('_author', 'Неизвестный автор')
                            readable_text += f"Цитата: {text}\nАвтор: {author}\n\n"
                        else:
                            readable_text += "Некорректные данные в элементе.\n\n"
                    
                    return readable_text if readable_text else "Нет данных для отображения."
                else:
                    return "Ответ не является списком."
            else:
                return "Ошибка при получении данных"

async def post_data_to_backend(endpoint):
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{BACKEND_URL}/{endpoint}") as response:
            if response.status == 200:
                return "Данные успешно сохранены"  # Возвращаем ответ от сервера
            else:
                return f"Ошибка при отправке данных: {response.status}"


# Хендлер команды /start
@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    # Создаем клавиатуру с кнопками (меню)
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = KeyboardButton("Рандомная цитата")
    button2 = KeyboardButton("Перевести цитату")
    button3 = KeyboardButton("Сохранить текущую цитату")
    button4 = KeyboardButton("Список сохраненных цитат")
    keyboard.add(button1, button2, button3, button4)

    await message.reply("Выберите действие:", reply_markup=keyboard)

# Хендлер для обработки выбранной кнопки
@dp.message_handler(lambda message: message.text in ["Рандомная цитата", "Перевести цитату", "Сохранить текущую цитату", "Список сохраненных цитат"])
async def menu_handler(message: types.Message):
    if message.text == "Рандомная цитата":
        text = await get_text_from_backend("random_quote")

    elif message.text == "Перевести цитату":
        text = await get_text_from_backend("translate")

    elif message.text == "Сохранить текущую цитату":
        text = await post_data_to_backend("save_quote")

    elif message.text == "Список сохраненных цитат":
        text = await get_all_text_from_backend("get_all_quotes")

    # Отправить результат пользователю
    await message.answer(text)

    # Задержка на 5 секунд (используем асинхронную задержку)
    await asyncio.sleep(5)

    # Удаляем сообщение, которое вызвало команду
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)


# Запуск бота
if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
