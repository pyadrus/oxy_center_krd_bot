from aiogram import types
from loguru import logger  # Логирование с помощью loguru

from keyboards.user_keyboards import appointment_selection_keypad
from system.dispatcher import bot
from system.dispatcher import dp  # Подключение к боту и диспетчеру пользователя


# conn = sqlite3.connect('your_database.db')
# cursor = conn.cursor()
# cursor.execute('''CREATE TABLE IF NOT EXISTS orders (id INTEGER PRIMARY KEY AUTOINCREMENT, surname TEXT, name TEXT, phone TEXT)''')


# Создание класса состояний
# class MakingAnOrder(StatesGroup):
#     write_name = State()  # Имя
#     write_surname = State()  # Фамилия
#
#
# class YourState(StatesGroup):
#     phone_input = State()  # Ввод номера телефона


@dp.callback_query_handler(lambda c: c.data == "sign_up")
async def sign_up_handler(callback_query: types.CallbackQuery):
    """Записаться"""
    try:
        sing_text = "Записаться на прием к специалисту вы можете по телефону или через оператора в чате!"
        appointment_selection_key = appointment_selection_keypad()
        await bot.send_message(callback_query.from_user.id, sing_text,
                               reply_markup=appointment_selection_key,
                               parse_mode=types.ParseMode.HTML,
                               disable_web_page_preview=True)
    except Exception as error:
        logger.exception(error)


# @dp.callback_query_handler(lambda c: c.data == "agree")
# async def agree_handler(callback_query: types.CallbackQuery, state: FSMContext):
#     """Записаться"""
#     await state.reset_state()
#     greeting_message = "Введите Вашу фамилию (желательно кириллицей)!\n"
#     await bot.send_message(callback_query.from_user.id, greeting_message)
#     await MakingAnOrder.write_surname.set()
#
#
# @dp.message_handler(state=MakingAnOrder.write_surname)
# async def write_surname_handler(message: types.Message, state: FSMContext):
#     """Обработчик ввода фамилии"""
#     surname = message.text
#     print(f"Фамилия: {surname}")
#     await state.update_data(surname=surname)
#     await bot.send_message(message.from_user.id, "Введите ваше Имя (желательно кириллицей)")
#     await MakingAnOrder.write_name.set()
#
#
# @dp.message_handler(state=MakingAnOrder.write_name)
# async def write_name_handler(message: types.Message, state: FSMContext):
#     """Обработчик ввода имени"""
#     user_id = message.from_user.id
#     surname = (await state.get_data())['surname']
#     name = message.text
#     text_mes = (f"Рады познакомиться {name} {surname}, пожалуйста,\n"
#                 "подтвердите, все ли Ваши данные верны!\n"
#                 f"Ваше имя: {name}\n"
#                 f"Ваша фамилия: {surname}\n"
#                 "Все верно?")
#     confirmation_keyboards = confirmation_keypad()  # Клавиатура, Верно не Верно
#     await bot.send_message(user_id, text_mes, reply_markup=confirmation_keyboards)
#
#
# @dp.callback_query_handler(lambda c: c.data == "faithfully")
# async def handle_faithfully(callback_query: types.CallbackQuery, state: FSMContext):
#     """Если все верно"""
#     try:
#         # Получаем данные из состояния FSMContext
#         async with state.proxy() as data:
#             surname = data['surname']
#             name = data['name']
#
#         # Вставляем данные пользователя в базу данных
#         conn = sqlite3.connect('your_database.db')
#         cursor = conn.cursor()
#         cursor.execute("INSERT INTO orders (surname, name, phone) VALUES (?, ?, ?)", (surname, name, None))
#         conn.commit()
#         conn.close()
#
#         sign_up_texts: str = "Записаться на прием к специалисту Вы можете по телефону или через оператора в чате!"
#         appointment_selection_key = appointment_selection_keypad()
#         await bot.send_message(callback_query.from_user.id, sign_up_texts,
#                                reply_markup=appointment_selection_key,
#                                parse_mode=types.ParseMode.HTML,
#                                disable_web_page_preview=True)
#     except Exception as error:
#         logger.exception(error)
#
#
# @dp.callback_query_handler(lambda c: c.data == "сall_key")
# async def call_handler(callback_query: types.CallbackQuery):
#     """Позвонить к специалисту"""
#     try:
#         sign_up_texts = ("Для связи с call-центром клиники наберите следующий номер: 8 (800) 550-98-17\n\n"
#                          "Для перехода в начальное меню нажмите /start")
#         await bot.send_message(callback_query.from_user.id, sign_up_texts,
#                                parse_mode=types.ParseMode.HTML,
#                                disable_web_page_preview=True)
#     except Exception as error:
#         logger.exception(error)
#
#
# @dp.callback_query_handler(lambda c: c.data == "callback_key")
# async def call_handler(callback_query: types.CallbackQuery):
#     """Заказать обратный звонок"""
#     try:
#         sign_up_texts = ("Для того чтобы заказать обратный звонок, поделитесь номером телефона нажав на кнопку или "
#                          "введите его вручную\n\n"
#                          "Для перехода в начальное меню нажмите /start")
#         markup = contact_keyboard()  # Используем клавиатуру для ручного ввода
#         await bot.send_message(callback_query.from_user.id, sign_up_texts,
#                                parse_mode=types.ParseMode.HTML,
#                                reply_markup=markup,  # Устанавливаем клавиатуру
#                                disable_web_page_preview=True)
#
#     except Exception as error:
#         logger.exception(error)
#
#
# @dp.message_handler(content_types=types.ContentType.CONTACT, state="*")
# async def handle_contact(message: types.Message):
#     """
#     Обработчик для получения контакта от пользователя, методом нажатия на кнопку 'Отправить контакт'
#     """
#     try:
#         markup = types.ReplyKeyboardRemove(selective=False)  # Удаляем клавиатуру
#         await message.answer("Спасибо за предоставленные данные. Мы свяжемся с вами в ближайшее время.",
#                              reply_markup=markup)
#         # Отправляем оповещение администратору или выполняем необходимые действия
#         admin_user_id = 535185511  # Замените на ID вашего администратора
#         await bot.send_message(admin_user_id,
#                                f"Пользователь {message.from_user.username} заказал обратный звонок: {message.contact.phone_number}")
#
#     except Exception as error:
#         logger.exception(error)
#
#
# @dp.message_handler(lambda message: message.text == "📝 Ввести вручную", state="*")
# async def manual_input_phone_handler(message: types.Message):
#     await message.answer("Введите ваш номер телефона в формате +1234567890")
#     # Set the state to capture the phone number input
#     await YourState.phone_input.set()
#
#
# @dp.message_handler(lambda message: message.text.startswith("+"), state=YourState.phone_input)
# async def handle_manual_phone_input(message: types.Message, state: FSMContext):
#     try:
#         phone_number = message.text
#         markup = types.ReplyKeyboardRemove(selective=False)  # Удаляем клавиатуру
#         await message.answer("Спасибо за предоставленные данные. Мы свяжемся с вами в ближайшее время.",
#                              reply_markup=markup)
#         # Отправляем оповещение администратору или выполняем необходимые действия
#         admin_user_id = 535185511  # Замените на ID вашего администратора
#         await bot.send_message(admin_user_id,
#                                f"Пользователь {message.from_user.username} заказал обратный звонок: {phone_number}")
#     except Exception as error:
#         logger.exception(error)





# @dp.callback_query_handler(lambda c: c.data == "confirm")
# async def call_handler(callback_query: types.CallbackQuery):
#     sign_up_text = ("Для связи с call-центром клиники наберите следующий номер: 8 (800) 550-98-17\n\n"
#                     "Для перехода в начальное меню нажмите /start")
#     await bot.send_message(callback_query.from_user.id, sign_up_text,
#                            parse_mode=ParseMode.HTML,
#                            disable_web_page_preview=True)












def register_callback_query_handler():
    """Регистрируем handlers для 'Записаться'"""
    dp.register_message_handler(sign_up_handler)
    # dp.register_message_handler(agree_handler)
    # dp.register_message_handler(handle_contact)
    # dp.register_message_handler(call_handler)
    # dp.register_message_handler(continue_recording)
