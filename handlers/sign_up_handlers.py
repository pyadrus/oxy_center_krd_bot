from aiogram.dispatcher.filters.state import StatesGroup, State
from loguru import logger  # Логирование с помощью loguru
from aiogram import types
from aiogram.dispatcher import FSMContext  # Состояния пользователя
from keyboards.user_keyboards import sign_up_keyboards, confirmation_keypad
from messages.user_messages import sign_up_text
from system.dispatcher import bot
from system.dispatcher import dp  # Подключение к боту и диспетчеру пользователя
import sqlite3

conn = sqlite3.connect('your_database.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS orders (id INTEGER PRIMARY KEY AUTOINCREMENT, surname TEXT, name TEXT, gender TEXT, phone TEXT)''')


@dp.callback_query_handler(lambda c: c.data == "sign_up")
async def sign_up_handler(callback_query: types.CallbackQuery):
    """Записаться"""
    try:
        keyboards_sign_up = sign_up_keyboards()
        await bot.send_message(callback_query.from_user.id, sign_up_text,
                               reply_markup=keyboards_sign_up,
                               parse_mode=types.ParseMode.HTML,
                               disable_web_page_preview=True)
    except Exception as error:
        logger.exception(error)


# Создание класса состояний
class MakingAnOrder(StatesGroup):
    write_name = State()  # Имя
    write_surname = State()  # Фамилия
    write_phone = State()  # Телефон
    write_gender = State()  # Пол


@dp.callback_query_handler(lambda c: c.data == "agree")
async def agree_handler(callback_query: types.CallbackQuery, state: FSMContext):
    """Записаться"""
    await state.reset_state()
    greeting_message = ("Введите Вашу фамилию (желательно кириллицей)!\n"
                        "Вы можете пропустить этот шаг\n\n")
    await bot.send_message(callback_query.from_user.id, greeting_message)
    await MakingAnOrder.write_surname.set()


# Обработчик ввода фамилии
@dp.message_handler(state=MakingAnOrder.write_surname)
async def write_surname_handler(message: types.Message, state: FSMContext):
    surname = message.text
    print(f"Фамилия: {surname}")
    await state.update_data(surname=surname)
    await bot.send_message(message.from_user.id, "Введите ваше Имя")
    await MakingAnOrder.write_name.set()


# Обработчик ввода имени
@dp.message_handler(state=MakingAnOrder.write_name)
async def write_name_handler(message: types.Message, state: FSMContext):
    name = message.text
    print(f"Имя: {name}")
    await state.update_data(name=name)
    await bot.send_message(message.from_user.id, "Введите ваш пол")
    await MakingAnOrder.write_gender.set()


# Обработчик ввода пола
@dp.message_handler(state=MakingAnOrder.write_gender)
async def write_gender_handler(message: types.Message, state: FSMContext):
    gender = message.text
    print(f"Пол: {gender}")
    await state.update_data(gender=gender)
    await bot.send_message(message.from_user.id, "Введите ваш номер телефона")
    await MakingAnOrder.write_phone.set()


# Обработчик ввода номера телефона
@dp.message_handler(state=MakingAnOrder.write_phone)
async def write_phone_handler(message: types.Message, state: FSMContext):
    phone = message.text
    print(f"Телефон: {phone}")
    async with state.proxy() as data:
        surname = data['surname']
        name = data['name']
        gender = data['gender']
    print(f"Записываемые данные: {name}, {surname}, {gender}, {phone}")
    # Вставка данных в таблицу базы данных
    cursor.execute("INSERT INTO orders (surname, name, gender, phone) VALUES (?, ?, ?, ?)",
                   (surname, name, gender, phone))
    conn.commit()
    # Закрытие соединения с базой данных
    conn.close()
    await state.finish()
    text_mes = (f"Ваш пол: {gender}\n\n"
                "Далее, пожалуйста, подтвердите, все ли Ваши данные верны!\n\n"
                f"Ваше имя: {name}\n"
                f"Ваша фамилия: {surname}\n"
                f"Ваш пол: {gender}\n"
                f"Ваш телефонный номер: {phone}\n"
                "Все верно?")
    confirmation_keyboards = confirmation_keypad()
    await bot.send_message(message.from_user.id, text_mes, reply_markup=confirmation_keyboards)


def register_callback_query_handler():
    """Регистрируем handlers для 'Записаться'"""
    dp.register_message_handler(sign_up_handler)
    dp.register_message_handler(agree_handler)
