import sqlite3
from datetime import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ParseMode, ReplyKeyboardMarkup, KeyboardButton

from keyboards.user_keyboards import create_sign_up_keyboard, create_data_modification_keyboard
from messages.user_messages import sign_up_text
from services.database import update_name_in_db, update_surname_in_db, update_city_in_db, get_user_data_from_db, \
    update_phone_in_db
from system.dispatcher import dp, bot


class MakingAnOrder(StatesGroup):
    """Создание класса состояний"""
    write_name = State()  # Имя
    write_surname = State()  # Фамилия
    phone_input = State()  # Передача номера телефона кнопкой
    write_city = State()  # Запись города


class ChangingData(StatesGroup):
    """Создание класса состояний, для смены данных пользователем"""
    changing_name = State()  # Имя
    changing_surname = State()  # Фамилия
    changing_phone = State()  # Передача номера телефона кнопкой
    changing_city = State()  # Запись города


@dp.callback_query_handler(lambda c: c.data == "my_details")
async def call_us_handler(callback_query: types.CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id  # Получаем ID текущего пользователя
    user_data = get_user_data_from_db(user_id)  # Функция, которая получает данные о пользователе из базы данных

    if user_data:
        # Если данные о пользователе найдены в базе данных, отобразите их
        name = user_data.get('name', 'не указано')
        surname = user_data.get('surname', 'не указано')
        city = user_data.get('city', 'не указано')
        phone_number = user_data.get('phone_number', 'не указано')
        registration_date = user_data.get('registration_date')

        text_mes = (f"🤝 Добро пожаловать, {name} {surname}! 🤝\n"
                    "Ваши данные:\n\n"
                    f"✅ <b>Имя:</b> {name}\n"
                    f"✅ <b>Фамилия:</b> {surname}\n"
                    f"✅ <b>Город:</b> {city}\n"
                    f"✅ <b>Номер телефона:</b> {phone_number}\n"
                    f"✅ <b>Дата регистрации:</b> {registration_date}\n\n"
                    "Для возврата нажмите /start")
        edit_data_keyboard = create_data_modification_keyboard()
        await bot.send_message(callback_query.from_user.id, text_mes,
                               reply_markup=edit_data_keyboard,
                               parse_mode=ParseMode.HTML)
    else:
        # Если данные о пользователе не найдены, предложите пройти регистрацию
        keyboards_sign_up = create_sign_up_keyboard()
        await bot.send_message(callback_query.from_user.id, sign_up_text,
                               reply_markup=keyboards_sign_up,
                               parse_mode=ParseMode.HTML,
                               disable_web_page_preview=True)


@dp.callback_query_handler(lambda c: c.data == "edit_name")
async def edit_name_handler(callback_query: types.CallbackQuery):
    # Отправляем сообщение с запросом на ввод нового имени и включаем состояние
    await bot.send_message(callback_query.from_user.id, "Введите новое имя:")
    await ChangingData.changing_name.set()


@dp.message_handler(state=ChangingData.changing_name)
async def process_entered_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        user_id = message.from_user.id
        new_name = message.text
        if update_name_in_db(user_id, new_name):
            text_name = (f"Имя успешно изменено на {new_name}\n\n"
                         f"Для возврата нажмите /start")
            await bot.send_message(user_id, text_name)
        else:
            text_name = (f"Произошла ошибка при изменении имени\n\n"
                         f"Для возврата нажмите /start")
            await bot.send_message(user_id, text_name)
        # Завершаем состояние после изменения имени
        await state.finish()


@dp.callback_query_handler(lambda c: c.data == "edit_surname")
async def edit_surname_handler(callback_query: types.CallbackQuery):
    # Отправляем сообщение с запросом на ввод нового имени и включаем состояние
    await bot.send_message(callback_query.from_user.id, "Введите новую фамилию:")
    await ChangingData.changing_surname.set()


@dp.message_handler(state=ChangingData.changing_surname)
async def process_entered_edit_surname(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        user_id = message.from_user.id
        new_surname = message.text
        if update_surname_in_db(user_id, new_surname):
            text_surname = (f"Фамилия успешно изменена на {new_surname}\n\n"
                            f"Для возврата нажмите /start")
            await bot.send_message(user_id, text_surname)
        else:
            text_surname = (f"Произошла ошибка при изменении фамилии\n\n"
                            f"Для возврата нажмите /start")
            await bot.send_message(user_id, text_surname)
        # Завершаем состояние после изменения имени
        await state.finish()


@dp.callback_query_handler(lambda c: c.data == "edit_city")
async def edit_city_handler(callback_query: types.CallbackQuery):
    # Отправляем сообщение с запросом на ввод нового имени и включаем состояние
    await bot.send_message(callback_query.from_user.id, "Введите новый город:")
    await ChangingData.changing_city.set()


@dp.message_handler(state=ChangingData.changing_city)
async def process_entered_edit_city(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        user_id = message.from_user.id
        new_city = message.text
        if update_city_in_db(user_id, new_city):
            text_city = (f"Фамилия успешно изменена на {new_city}\n\n"
                         f"Для возврата нажмите /start")
            await bot.send_message(user_id, text_city)
        else:
            text_city = (f"Произошла ошибка при изменении города\n\n"
                         f"Для возврата нажмите /start")
            await bot.send_message(user_id, text_city)
        # Завершаем состояние после изменения имени
        await state.finish()


@dp.callback_query_handler(lambda c: c.data == "edit_phone")
async def edit_city_handler(callback_query: types.CallbackQuery):
    # Отправляем сообщение с запросом на ввод нового имени и включаем состояние
    await bot.send_message(callback_query.from_user.id, "Введите новый номер телефона:")
    await ChangingData.changing_phone.set()


@dp.message_handler(state=ChangingData.changing_phone)
async def process_entered_edit_city(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        user_id = message.from_user.id
        new_phone = message.text
        if update_phone_in_db(user_id, new_phone):
            text_phone = (f"Номер телефона успешно изменен на {new_phone}\n\n"
                          f"Для возврата нажмите /start")
            await bot.send_message(user_id, text_phone)
        else:
            text_phone = (f"Произошла ошибка при изменении номера телефона\n\n"
                          f"Для возврата нажмите /start")
            await bot.send_message(user_id, text_phone)
        # Завершаем состояние после изменения имени
        await state.finish()


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
    await state.update_data(city=city)
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
    # Получение ID аккаунта Telegram
    user_id = message.from_user.id
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
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (user_id INTEGER,
                                                        name TEXT,
                                                        surname TEXT,
                                                        city TEXT,
                                                        phone_number TEXT,
                                                        registration_date TEXT)''')
    cursor.execute("INSERT INTO users (user_id, name, surname, city, phone_number, registration_date) "
                   "VALUES (?, ?, ?, ?, ?, ?)",
                   (user_id, name, surname, city, phone_number, registration_date))
    conn.commit()
    conn.close()
    await state.finish()  # Завершаем текущее состояние машины состояний
    await state.reset_state()  # Сбрасываем все данные машины состояний, до значения по умолчанию
    await bot.send_message(message.from_user.id, text_mes)


def register_my_detalist_handler():
    """Регистрируем handlers для 'Записаться'"""
    dp.register_message_handler(call_us_handler)
    dp.register_message_handler(edit_name_handler)
