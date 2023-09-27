import sqlite3

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ParseMode
from loguru import logger  # Логирование с помощью loguru

from keyboards.user_keyboards import appointment_selection_keypad, create_my_details_keyboard
from system.dispatcher import bot
from system.dispatcher import dp  # Подключение к боту и диспетчеру пользователя


def check_user_exists_in_db(user_id):
    # Подключитесь к вашей базе данных
    conn = sqlite3.connect("your_database.db")  # Замените "your_database.db" на имя вашей базы данных
    cursor = conn.cursor()
    # Выполните SQL-запрос для проверки наличия пользователя в базе данных по его user_id
    cursor.execute("SELECT COUNT(*) FROM users WHERE user_id = ?", (user_id,))
    # Извлеките результат запроса
    user_count = cursor.fetchone()[0]
    conn.close()
    # Если пользователь с указанным user_id найден (user_count больше 0), верните True, иначе верните False
    return user_count > 0


def get_user_data_from_db(user_id):
    # Замените "your_database.db" на имя вашей базы данных
    conn = sqlite3.connect("your_database.db")
    cursor = conn.cursor()
    # Выполните SQL-запрос для получения данных о пользователе по его user_id
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    user_data = cursor.fetchone()  # Получите данные первой найденной записи
    conn.close()

    # Верните данные о пользователе как словарь, если они существуют, или None, если пользователя нет
    if user_data:
        user_id, name, surname, city, phone_number, registration_date = user_data
        return {'user_id': user_id, 'name': name, 'surname': surname, 'city': city, 'phone_number': phone_number,
                'registration_date': registration_date}
    else:
        return None


@dp.callback_query_handler(lambda c: c.data == "sign_up")
async def sign_up_handler(callback_query: types.CallbackQuery):
    """Записаться"""
    try:
        sing_text = ("Записаться на прием к специалисту вы можете по телефону или через оператора в чате.\n\n"
                     f"Для возврата нажмите /start")
        appointment_selection_key = appointment_selection_keypad()
        await bot.send_message(callback_query.from_user.id, sing_text,
                               reply_markup=appointment_selection_key,
                               parse_mode=types.ParseMode.HTML,
                               disable_web_page_preview=True)
    except Exception as error:
        logger.exception(error)


# Обработчик callback-запроса
@dp.callback_query_handler(lambda c: c.data == "call_us")
async def call_handler(callback_query: types.CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id  # Получаем ID текущего пользователя
    user_exists = check_user_exists_in_db(user_id)  # Проверяем наличие пользователя в базе данных

    if user_exists:
        # Если пользователь существует, отправляем сообщение с номером телефона
        sign_up_text = ("Для связи с call-центром клиники наберите следующий номер: 8 (800) 550-98-17\n\n"
                        "Для перехода в начальное меню нажмите /start")
        # Отправляем сообщение с номером телефона или сообщением о регистрации
        await bot.send_message(callback_query.from_user.id, sign_up_text,
                               parse_mode=ParseMode.HTML,
                               disable_web_page_preview=True)
    else:
        # Если пользователя нет в базе данных, предлагаем пройти регистрацию
        sign_up_text = ("⚠️ <b>Вы не зарегистрированы в нашей системе</b> ⚠️\n\n"
                        "Для доступа к этому разделу, пожалуйста, <b>зарегистрируйтесь</b> в меню 'Мои данные'.\n\n"
                        "Для перехода в начальное меню нажмите /start")

        # Создаем клавиатуру с помощью my_details() (предполагается, что она существует)
        my_details_key = create_my_details_keyboard()
        # Отправляем сообщение с предложением зарегистрироваться и клавиатурой
        await bot.send_message(callback_query.from_user.id, sign_up_text,
                               reply_markup=my_details_key,
                               parse_mode=ParseMode.HTML,
                               disable_web_page_preview=True)


@dp.callback_query_handler(lambda c: c.data == "callback_key")
async def callback_key_handler(callback_query: types.CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id  # Получаем ID текущего пользователя
    user_exists = check_user_exists_in_db(user_id)  # Функция, которая проверяет наличие пользователя в базе данных
    if user_exists:
        user_data = get_user_data_from_db(user_id)  # Получите данные пользователя из базы данных
        name = user_data.get('name', 'не указано')
        surname = user_data.get('surname', 'не указано')
        phone_number = user_data.get('phone_number', 'не указано')

        # Отправьте уведомление администратору с данными пользователя
        admin_user_id = 535185511  # Замените на ID администратора
        message_text = (f"Пользователь {name} {surname} заказал обратный звонок.\n"
                        f"Номер телефона для обратной связи: {phone_number}")
        await bot.send_message(admin_user_id, message_text)
        sign_up_text = ("✅ Ваши данные успешно переданы оператору. В ближайшее время мы с вами свяжемся.\n"
                        "Изменить данные вы можете в меню 'Мои данные'.\n\n"
                        "Для перехода в начальное меню нажмите /start")
        await bot.send_message(callback_query.from_user.id, sign_up_text,
                               parse_mode=ParseMode.HTML,
                               disable_web_page_preview=True)
    else:
        sign_up_text = ("⚠️ <b>Вы не зарегистрированы в нашей системе</b> ⚠️\n\n"
                        "Для доступа к этому разделу, пожалуйста, <b>зарегистрируйтесь</b> в меню 'Мои данные'.\n\n"
                        "Для перехода в начальное меню нажмите /start")
        # Создаем клавиатуру с помощью my_details() (предполагается, что она существует)
        my_details_key = create_my_details_keyboard()
        # Отправляем сообщение с предложением зарегистрироваться и клавиатурой
        await bot.send_message(callback_query.from_user.id, sign_up_text,
                               reply_markup=my_details_key,
                               parse_mode=ParseMode.HTML,
                               disable_web_page_preview=True)


def register_callback_query_handler():
    """Регистрируем handlers для 'Записаться'"""
    dp.register_message_handler(sign_up_handler)
    dp.register_message_handler(call_handler)
    dp.register_message_handler(callback_key_handler)
