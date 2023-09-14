from aiogram import types
from aiogram.dispatcher import FSMContext  # Состояния пользователя
from loguru import logger # Логирование с помощью loguru

from keyboards.user_keyboards import greeting_keyboards  # Клавиатуры поста приветствия
from system.dispatcher import dp  # Подключение к боту и диспетчеру пользователя


@dp.message_handler(commands=['start'])
async def greeting(message: types.Message, state: FSMContext):
    """Обработчик команды /start, он же пост приветствия 👋"""
    try:
        await state.finish() # Завершаем текущее состояние машины состояний
        await state.reset_state() # Сбрасываем все данные машины состояний, до значения по умолчанию

        from_user_name = message.from_user.first_name  # Получаем фамилию пользователя
        greeting_post = (f"{from_user_name}, Вас приветствует чат-бот клиники мужского и женского здоровья "
                         f"<b>OXY center!</b>")
        keyboards_greeting = greeting_keyboards()  # Клавиатуры поста приветствия 👋
        with open("media/photos/logo.jpg", "rb") as photo_file:
            await message.reply_photo(photo_file,  # Изображение в посте приветствия 👋
                                      caption=greeting_post,  # Текст для приветствия 👋
                                      reply_markup=keyboards_greeting,  # Клавиатура приветствия 👋
                                      parse_mode=types.ParseMode.HTML)  # Текст в HTML-разметки
    except Exception as e:
        logger.exception(e)


def greeting_handler():
    """Регистрируем handlers для бота"""
    dp.register_message_handler(greeting)  # Обработчик команды /start, он же пост приветствия 👋
