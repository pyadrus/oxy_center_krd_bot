from aiogram import types
# from aiogram.dispatcher import FSMContext
# from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ParseMode, ReplyKeyboardMarkup, KeyboardButton

from keyboards.user_keyboards import sign_up_keyboards
from messages.user_messages import sign_up_text
# from services.database import writing_to_the_database
from system.dispatcher import dp, bot


# Создание класса состояний
# class MakingAnOrder(StatesGroup):
#     write_name = State()  # Имя
#     write_surname = State()  # Фамилия
#     phone_input = State()  # Передача номера телефона кнопкой


@dp.callback_query_handler(lambda c: c.data == "call_us")
async def call_us_handler(callback_query: types.CallbackQuery):
    keyboards_sign_up = sign_up_keyboards()
    await bot.send_message(callback_query.from_user.id, sign_up_text,
                           reply_markup=keyboards_sign_up,
                           parse_mode=ParseMode.HTML,
                           disable_web_page_preview=True)


# @dp.callback_query_handler(lambda c: c.data == "agree")
# async def agree_handler(callback_query: types.CallbackQuery, state: FSMContext):
#
#     await state.reset_state()
#     await MakingAnOrder.write_surname.set()
#     await bot.send_message(callback_query.from_user.id, "Введите Вашу Фамилию (желательно кириллицей)!")
#
#
# @dp.message_handler(state=MakingAnOrder.write_surname)
# async def write_surname_handler(message: types.Message, state: FSMContext):
#     surname = message.text
#     await state.update_data(surname=surname)
#     await MakingAnOrder.write_name.set()
#     await bot.send_message(message.from_user.id, "Введите Ваше Имя (желательно кириллицей)")
#
#
# @dp.message_handler(state=MakingAnOrder.write_name)
# async def write_name_handler(message: types.Message, state: FSMContext):
#     name = message.text
#     await state.update_data(name=name)
#     # await MakingAnOrder.phone_input.set()
#     sign_up_texts = "Для ввода номера телефона вы можете поделиться номером телефона нажав на кнопку или ввести его\n\n"
#     markup = ReplyKeyboardMarkup(resize_keyboard=True)
#     # Добавьте кнопку для отправки контакта
#     send_contact_button = KeyboardButton("📱 Отправить", request_contact=True)
#     # Добавление кнопки для ручного ввода
#     markup.add(send_contact_button)
#     await bot.send_message(message.from_user.id, sign_up_texts,
#                            reply_markup=markup,  # Set the custom keyboard
#                            parse_mode=types.ParseMode.HTML,
#                            disable_web_page_preview=True)
#     await MakingAnOrder.phone_input.set()
#
#
# @dp.message_handler(content_types=types.ContentType.CONTACT, state=MakingAnOrder.phone_input)
# async def handle_contact(message: types.Message, state: FSMContext):
#     phone_number = message.contact.phone_number
#     await state.update_data(phone_number=phone_number)
#     await handle_confirmation(message, state)
#
#
# @dp.message_handler(lambda message: message.text and not message.contact, state=MakingAnOrder.phone_input)
# async def handle_phone_text(message: types.Message, state: FSMContext):
#     phone_number = message.text
#     await state.update_data(phone_number=phone_number)
#     await handle_confirmation(message, state)
#
#
# async def handle_confirmation(message: types.Message, state: FSMContext):
#     markup = types.ReplyKeyboardRemove(selective=False)  # Remove the keyboard
#     await message.answer("Спасибо за предоставленные данные.", reply_markup=markup)
#     # Извлечение пользовательских данных из состояния
#     user_data = await state.get_data()
#     surname = user_data.get('surname', 'не указан')
#     name = user_data.get('name', 'не указан')
#     phone_number = user_data.get('phone_number', 'не указан')
#     # Составьте подтверждающее сообщение
#     text_mes = (f"Рады познакомиться {name} {surname}, пожалуйста,\n"
#                 "подтвердите, все ли Ваши данные верны!\n"
#                 f"Ваше имя: {name}\n"
#                 f"Ваша фамилия: {surname}\n"
#                 f"Ваш номер телефона: {phone_number}\n"
#                 "Если данные не верны, то нажмите на кнопку изменить данные")
#     confirmation_keyboard = types.InlineKeyboardMarkup()
#     confirmation_keyboard.add(types.InlineKeyboardButton(text="Изменить данные", callback_data="agree"))
#     writing_to_the_database(surname, name, phone_number)
#     await bot.send_message(message.from_user.id, text_mes, reply_markup=confirmation_keyboard)


def register_call_us_handler():
    """Регистрируем handlers для 'Записаться'"""
    dp.register_message_handler(call_us_handler)
    dp.register_message_handler(agree_handler)
