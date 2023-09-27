from aiogram import types
from loguru import logger

from messages.user_messages import contacts_and_address_text
from system.dispatcher import dp, bot


@dp.callback_query_handler(lambda c: c.data == 'contacts_and_address')
async def contacts_and_address_handler(callback_query: types.CallbackQuery):
    """Контакты и адрес"""
    try:
        await bot.send_message(callback_query.from_user.id, contacts_and_address_text, parse_mode=types.ParseMode.HTML,
                               disable_web_page_preview=True)
    except Exception as error:
        logger.exception(error)


def register_contacts_and_address_handler():
    """Регистрируем handlers для 'Контакты и адрес'"""
    dp.register_message_handler(contacts_and_address_handler)
