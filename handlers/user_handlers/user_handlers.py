from aiogram import types
from aiogram.dispatcher import FSMContext  # Состояния пользователя
from loguru import logger  # Логирование с помощью loguru

from keyboards.user_keyboards import create_greeting_keyboard  # Клавиатуры поста приветствия
from system.dispatcher import dp  # Подключение к боту и диспетчеру пользователя


@dp.message_handler(commands=['start'])
async def greeting(message: types.Message, state: FSMContext):
    """Обработчик команды /start, он же пост приветствия 👋"""
    try:
        await state.finish()  # Завершаем текущее состояние машины состояний
        await state.reset_state()  # Сбрасываем все данные машины состояний, до значения по умолчанию

        from_user_name = message.from_user.first_name  # Получаем фамилию пользователя
        greeting_post = (f"{from_user_name}, Вас приветствует чат-бот клиники мужского и женского здоровья "
                         f"<b>OXY center!</b>")
        keyboards_greeting = create_greeting_keyboard()  # Клавиатуры поста приветствия 👋
        with open("media/photos/logo.jpg", "rb") as photo_file:
            await message.reply_photo(photo_file,  # Изображение в посте приветствия 👋
                                      caption=greeting_post,  # Текст для приветствия 👋
                                      reply_markup=keyboards_greeting,  # Клавиатура приветствия 👋
                                      parse_mode=types.ParseMode.HTML)  # Текст в HTML-разметки
    except Exception as error:
        logger.exception(error)


@dp.callback_query_handler(lambda c: c.data == "disagree")
async def disagree_handler(callback_query: types.CallbackQuery, state: FSMContext):
    try:
        await state.finish()  # Завершаем текущее состояние машины состояний
        await state.reset_state()  # Сбрасываем все данные машины состояний, до значения по умолчанию

        from_user_name = callback_query.from_user.first_name  # Получаем имя пользователя из callback_query
        greeting_post = (f"{from_user_name}, Вас приветствует чат-бот клиники мужского и женского здоровья "
                         f"<b>OXY center!</b>")
        keyboards_greeting = create_greeting_keyboard()  # Клавиатуры поста приветствия 👋
        with open("media/photos/logo.jpg", "rb") as photo_file:
            await callback_query.message.reply_photo(photo_file,  # Изображение в посте приветствия 👋
                                                     caption=greeting_post,  # Текст для приветствия 👋
                                                     reply_markup=keyboards_greeting,  # Клавиатура приветствия 👋
                                                     parse_mode=types.ParseMode.HTML)  # Текст в HTML-разметки
    except Exception as error:
        logger.exception(error)


def greeting_handler():
    """Регистрируем handlers для бота"""
    dp.register_message_handler(greeting)  # Обработчик команды /start, он же пост приветствия 👋
    dp.register_message_handler(disagree_handler)
