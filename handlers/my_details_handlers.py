import sqlite3

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ParseMode, ReplyKeyboardMarkup, KeyboardButton

from keyboards.user_keyboards import sign_up_keyboards
from messages.user_messages import sign_up_text
from services.database import writing_to_the_database
from system.dispatcher import dp, bot
from datetime import datetime


# Функция для создания таблицы, если она не существует
def create_table_if_not_exists():
    conn = sqlite3.connect("your_database.db")  # Замените "your_database.db" на имя вашей базы данных
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT,
            surname TEXT,
            city TEXT,
            phone_number TEXT,
            registration_date TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Создание класса состояний
class MakingAnOrder(StatesGroup):
    write_name = State()  # Имя
    write_surname = State()  # Фамилия
    phone_input = State()  # Передача номера телефона кнопкой
    write_city = State()  # Запись города


@dp.callback_query_handler(lambda c: c.data == "my_details")
async def call_us_handler(callback_query: types.CallbackQuery):
    keyboards_sign_up = sign_up_keyboards()
    await bot.send_message(callback_query.from_user.id, sign_up_text,
                           reply_markup=keyboards_sign_up,
                           parse_mode=ParseMode.HTML,
                           disable_web_page_preview=True)


@dp.callback_query_handler(lambda c: c.data == "agree")
async def agree_handler(callback_query: types.CallbackQuery, state: FSMContext):
    await state.reset_state()
    await MakingAnOrder.write_surname.set()
    text_mes = (f"👥 Введите вашу фамилию (желательно кириллицей):\n"
                "Пример: Петров, Иванова, Сидоренко")
    await bot.send_message(callback_query.from_user.id, text_mes)


@dp.message_handler(state=MakingAnOrder.write_surname)
async def write_surname_handler(message: types.Message, state: FSMContext):
    surname = message.text
    await state.update_data(surname=surname)
    await MakingAnOrder.write_name.set()
    text_mes = (f"👤 Введите ваше имя (желательно кириллицей):\n"
                "Пример: Иван, Ольга, Анастасия")
    await bot.send_message(message.from_user.id, text_mes)


@dp.message_handler(state=MakingAnOrder.write_name)
async def write_city_handlers(message: types.Message, state: FSMContext):
    name = message.text
    await state.update_data(name=name)
    await MakingAnOrder.write_city.set()
    text_mes = (f"🏙️ Введите ваш город (желательно кириллицей):\n"
                "Пример: Москва, Санкт-Петербург")
    await bot.send_message(message.from_user.id, text_mes)


@dp.message_handler(state=MakingAnOrder.write_city)
async def write_name_handler(message: types.Message, state: FSMContext):
    city = message.text
    await state.update_data(name=city)
    sign_up_texts = (
        "Для ввода номера телефона вы можете поделиться номером телефона, нажав на кнопку или ввести его вручную.\n\n"
        "Чтобы ввести номер вручную, просто отправьте его в текстовом поле.")
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    # Добавьте кнопку для отправки контакта
    send_contact_button = KeyboardButton("📱 Отправить", request_contact=True)
    # Добавление кнопки для ручного ввода
    markup.add(send_contact_button)
    await bot.send_message(message.from_user.id, sign_up_texts,
                           reply_markup=markup,  # Set the custom keyboard
                           parse_mode=types.ParseMode.HTML,
                           disable_web_page_preview=True)
    await MakingAnOrder.phone_input.set()


@dp.message_handler(content_types=types.ContentType.CONTACT, state=MakingAnOrder.phone_input)
async def handle_contact(message: types.Message, state: FSMContext):
    phone_number = message.contact.phone_number
    await state.update_data(phone_number=phone_number)
    await handle_confirmation(message, state)


@dp.message_handler(lambda message: message.text and not message.contact, state=MakingAnOrder.phone_input)
async def handle_phone_text(message: types.Message, state: FSMContext):
    phone_number = message.text
    await state.update_data(phone_number=phone_number)
    await handle_confirmation(message, state)


async def handle_confirmation(message: types.Message, state: FSMContext):
    markup = types.ReplyKeyboardRemove(selective=False)  # Remove the keyboard
    await message.answer("Спасибо за предоставленные данные.", reply_markup=markup)
    # Извлечение пользовательских данных из состояния
    user_data = await state.get_data()
    surname = user_data.get('surname', 'не указан')
    name = user_data.get('name', 'не указан')
    phone_number = user_data.get('phone_number', 'не указан')
    city = user_data.get('city', 'не указан')
    registration_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Составьте подтверждающее сообщение
    text_mes = (f"🤝 Рады познакомиться {name} {surname}! 🤝\n"
                "Пожалуйста, подтвердите, все ли Ваши данные верны:\n\n"
                f"✅ <b>Ваше Имя:</b> {name}\n"
                f"✅ <b>Ваша Фамилия:</b> {surname}\n"
                f"✅ <b>Ваш Город:</b> {city}\n"
                f"✅ <b>Ваш номер телефона:</b> {phone_number}\n"
                f"✅ <b>Ваша Дата регистрации:</b> {registration_date}\n\n"
                "Если данные не верны, то вы можете всегда изменить.\n\n"
                "Для возврата нажмите /start")
    # Запись данных в базу данных
    conn = sqlite3.connect("your_database.db")  # Замените "your_database.db" на имя вашей базы данных
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name, surname, city, phone_number, registration_date) VALUES (?, ?, ?, ?, ?)",
                   (name, surname, city, phone_number, registration_date))
    conn.commit()
    conn.close()

    await bot.send_message(message.from_user.id, text_mes)


def register_my_detalist_handler():
    """Регистрируем handlers для 'Записаться'"""
    dp.register_message_handler(call_us_handler)
