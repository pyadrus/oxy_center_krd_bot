from aiogram import types
from loguru import logger

from keyboards.user_keyboards import sign_up_keyboards
from messages.user_messages import sign_up_text
from system.dispatcher import dp, bot


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


def register_callback_query_handler():
    """Регистрируем handlers для 'Записаться'"""
    dp.register_message_handler(sign_up_handlers)
