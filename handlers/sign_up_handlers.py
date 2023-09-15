from aiogram.dispatcher.filters.state import StatesGroup, State
from loguru import logger  # Логирование с помощью loguru
from aiogram import types
from aiogram.dispatcher import FSMContext  # Состояния пользователя
from keyboards.user_keyboards import sign_up_keyboards
from messages.user_messages import sign_up_text
from system.dispatcher import bot
from system.dispatcher import dp  # Подключение к боту и диспетчеру пользователя


@dp.callback_query_handler(lambda c: c.data == "sign_up")
async def sign_up_handlers(callback_query: types.CallbackQuery):
    """Записаться"""
    try:
        keyboards_sign_up = sign_up_keyboards()
        await bot.send_message(callback_query.from_user.id, sign_up_text,
                               reply_markup=keyboards_sign_up,
                               parse_mode=types.ParseMode.HTML,
                               disable_web_page_preview=True)
    except Exception as e:
        logger.exception(e)


# Создание класса состояний
class MakingAnOrder(StatesGroup):
    making_an_order = State()
    write_name = State()  # Имя
    write_surname = State()  # Фамилия
    write_phone = State()
    write_gender = State()


@dp.callback_query_handler(lambda c: c.data == "agree")
async def agree_handlers(callback_query: types.CallbackQuery, state: FSMContext):
    """Записаться"""
    await state.reset_state()
    greeting_post_on = ("Введите Вашу фамилию (желательно кириллицей)!\n"
                        "Вы можете пропустить этот шаг\n\n")
    await bot.send_message(callback_query.from_user.id, greeting_post_on)
    await MakingAnOrder.write_name.set()


# Обработчик ввода имени
@dp.message_handler(state=MakingAnOrder.write_name)
async def write_name(message: types.Message, state: FSMContext):
    name = message.text
    print(f"Фамилия: {name}")
    await state.update_data(name=name)
    await MakingAnOrder.next()
    await bot.send_message(message.from_user.id, "Введите ваше Имя")


@dp.message_handler(state=MakingAnOrder.write_surname)
async def write_name(message: types.Message, state: FSMContext):
    surname = message.text
    print(f"Имя: {surname}")
    await state.update_data(name=surname)
    await MakingAnOrder.next()
    await bot.send_message(message.from_user.id, "Введите ваш пол")


@dp.message_handler(state=MakingAnOrder.write_gender)
async def write_name(message: types.Message, state: FSMContext):
    gender = message.text
    print(f"Пол: {gender}")
    await state.update_data(name=gender)
    await MakingAnOrder.next()
    await bot.send_message(message.from_user.id, "Введите ваш номер телефона")


@dp.message_handler(state=MakingAnOrder.write_phone)
async def write_name(message: types.Message, state: FSMContext):
    phone = message.text
    print(f"Телефон: {phone}")
    await state.update_data(name=phone)
    await MakingAnOrder.next()
    await bot.send_message(message.from_user.id, "Введите ваш номер телефона")


def register_callback_query_handler():
    """Регистрируем handlers для 'Записаться'"""
    dp.register_message_handler(sign_up_handlers)
    dp.register_message_handler(agree_handlers)
