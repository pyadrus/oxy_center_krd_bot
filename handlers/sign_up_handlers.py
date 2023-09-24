import sqlite3

from aiogram import types
from aiogram.dispatcher import FSMContext  # Состояния пользователя
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from loguru import logger  # Логирование с помощью loguru

from keyboards.user_keyboards import sign_up_keyboards, confirmation_keypad, appointment_selection_keypad
from messages.user_messages import sign_up_text
from system.dispatcher import bot
from system.dispatcher import dp  # Подключение к боту и диспетчеру пользователя

conn = sqlite3.connect('your_database.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS orders (
                  id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  surname TEXT, 
                  name TEXT)''')


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


@dp.callback_query_handler(lambda c: c.data == "agree")
async def agree_handler(callback_query: types.CallbackQuery, state: FSMContext):
    """Записаться"""
    await state.reset_state()
    greeting_message = ("Введите Вашу фамилию (желательно кириллицей)!\n"
                        "Вы можете пропустить этот шаг\n\n")
    await bot.send_message(callback_query.from_user.id, greeting_message)
    await MakingAnOrder.write_surname.set()


@dp.message_handler(state=MakingAnOrder.write_surname)
async def write_surname_handler(message: types.Message, state: FSMContext):
    """Обработчик ввода фамилии"""
    surname = message.text
    print(f"Фамилия: {surname}")
    await state.update_data(surname=surname)
    await bot.send_message(message.from_user.id, "Введите ваше Имя")
    await MakingAnOrder.write_name.set()


@dp.message_handler(state=MakingAnOrder.write_name)
async def write_name_handler(message: types.Message, state: FSMContext):
    """Обработчик ввода имени"""
    try:
        async with state.proxy() as data:
            surname = data['surname']
        name = message.text
        print(f"Записываемые данные: {name}, {surname}")
        # Вставка данных в таблицу базы данных
        cursor.execute("INSERT INTO orders (surname, name) VALUES (?, ?)", (surname, name))
        conn.commit()
        conn.close()  # Закрытие соединения с базой данных
        await state.finish()
        text_mes = (f"Рады познакомиться {name} {surname}, пожалуйста,\n"
                    "подтвердите, все ли Ваши данные верны!\n"
                    f"Ваше имя: {name}\n"
                    f"Ваша фамилия: {surname}\n"
                    "Все верно?")
        confirmation_keyboards = confirmation_keypad()
        await bot.send_message(message.from_user.id, text_mes, reply_markup=confirmation_keyboards)
    except Exception as e:
        logger.exception(e)


@dp.callback_query_handler(lambda c: c.data == "faithfully")
async def continue_recording(callback_query: types.CallbackQuery):
    try:
        sign_up_texts: str = "Записаться на прием к специалисту Вы можете по телефону или через оператора в чате!"
        appointment_selection_key = appointment_selection_keypad()
        await bot.send_message(callback_query.from_user.id, sign_up_texts,
                               reply_markup=appointment_selection_key,
                               parse_mode=types.ParseMode.HTML,
                               disable_web_page_preview=True)
    except Exception as error:
        logger.exception(error)


@dp.callback_query_handler(lambda c: c.data == "сall_key")
async def call_handler(callback_query: types.CallbackQuery):
    """Позвонить к специалисту"""
    try:
        sign_up_texts = ("Для связи с call-центром клиники наберите следующий номер: 8 (800) 550-98-17\n\n"
                         "Для перехода в начальное меню нажмите /start")
        await bot.send_message(callback_query.from_user.id, sign_up_texts,
                               parse_mode=types.ParseMode.HTML,
                               disable_web_page_preview=True)
    except Exception as error:
        logger.exception(error)


def contact_keyboard():
    """Клавиатура отправки отчетов"""
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    first_button = KeyboardButton(text="📱 Отправить", request_contact=True)
    markup.add(first_button)
    return markup

@dp.callback_query_handler(lambda c: c.data == "callback_key")
async def call_handler(callback_query: types.CallbackQuery):
    """Заказать обратный звонок"""
    try:
        sign_up_texts = ("Для того чтобы заказать обратный звонок, поделитесь номером телефона нажав на кнопку или "
                         "введите его вручную\n\n"
                         "Для перехода в начальное меню нажмите /start")
        markup = contact_keyboard()  # Используем клавиатуру для ручного ввода
        await bot.send_message(callback_query.from_user.id, sign_up_texts,
                               parse_mode=types.ParseMode.HTML,
                               reply_markup=markup,  # Устанавливаем клавиатуру
                               disable_web_page_preview=True)

    except Exception as error:
        logger.exception(error)


@dp.message_handler(content_types=types.ContentType.CONTACT, state="*")
async def handle_contact(message: types.Message):
    """
    Обработчик для получения контакта от пользователя, методом нажатия на кнопку 'Отправить контакт'
    """
    try:
        # Удаляем клавиатуру
        markup = types.ReplyKeyboardRemove(selective=False)
        await message.answer("Спасибо за предоставленные данные. Мы свяжемся с вами в ближайшее время.",
                             reply_markup=markup)
        # Отправляем оповещение администратору или выполняем необходимые действия
        admin_user_id = 535185511  # Замените на ID вашего администратора
        await bot.send_message(admin_user_id, f"Пользователь {message.from_user.username} заказал обратный звонок: {message.contact.phone_number}")

    except Exception as error:
        logger.exception(error)


def register_callback_query_handler():
    """Регистрируем handlers для 'Записаться'"""
    dp.register_message_handler(sign_up_handler)
    dp.register_message_handler(agree_handler)
    dp.register_message_handler(handle_contact)
    dp.register_message_handler(call_handler)
