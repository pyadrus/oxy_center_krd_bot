from aiogram import types
from aiogram.dispatcher import FSMContext  # Состояния пользователя
from loguru import logger

from keyboards.user_keyboards import greeting_keyboards  # Клавиатуры поста приветствия
from system.dispatcher import dp  # Подключение к боту и диспетчеру пользователя


@dp.message_handler(commands=['start'])
async def greeting(message: types.Message, state: FSMContext):
    """Обработчик команды /start, он же пост приветствия"""
    try:
        await state.finish()
        await state.reset_state()

        # Получаем имя пользователя
        from_user_name = message.from_user.first_name
        greeting_post = (f"{from_user_name}, Вас приветствует чат-бот клиники мужского и женского здоровья <b>OXY center!</b>")

        keyboards_greeting = greeting_keyboards()
        await message.reply(greeting_post, reply_markup=keyboards_greeting, disable_web_page_preview=True,
                            parse_mode=types.ParseMode.HTML)
    except Exception as e:
        logger.exception(e)


def greeting_handler():
    """Регистрируем handlers для бота"""
    dp.register_message_handler(greeting)  # Обработчик команды /start, он же пост приветствия
