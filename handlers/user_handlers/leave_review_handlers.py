from aiogram import types
from loguru import logger

from messages.user_messages import leave_review_text
from system.dispatcher import dp, bot


@dp.callback_query_handler(lambda c: c.data == 'leave_review')
async def leave_review_handler(callback_query: types.CallbackQuery):
    """Оставить отзыв"""
    try:
        await bot.send_message(callback_query.from_user.id, leave_review_text, parse_mode=types.ParseMode.HTML, disable_web_page_preview=True)
    except Exception as error:
        logger.exception(error)


def register_leave_review_handler():
    """Регистрируем handlers для 'Оставить отзыв'"""
    dp.register_message_handler(leave_review_handler)
