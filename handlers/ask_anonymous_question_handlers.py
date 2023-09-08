from aiogram import types
from loguru import logger

from messages.user_messages import ask_anonymous_question_text
from system.dispatcher import dp, bot


@dp.callback_query_handler(lambda c: c.data == 'ask_anonymous_question')
async def ask_anonymous_question_handler(callback_query: types.CallbackQuery):
    """Задать анонимный вопрос"""
    try:
        await bot.send_message(callback_query.from_user.id, ask_anonymous_question_text,
                               parse_mode=types.ParseMode.HTML, disable_web_page_preview=True)
    except Exception as e:
        logger.exception(e)


def register_ask_anonymous_question_handler():
    """Регистрируем handlers для 'Задать анонимный вопрос'"""
    dp.register_message_handler(ask_anonymous_question_handler)
