from aiogram import types

from messages.user_messages import current_promotions_text
from system.dispatcher import dp, bot


@dp.callback_query_handler(lambda c: c.data == 'current_promotions')
async def current_promotions_handler(callback_query: types.CallbackQuery):
    """Текущие акции"""
    await bot.send_message(callback_query.from_user.id, current_promotions_text, parse_mode=types.ParseMode.HTML)


def register_current_promotions_handler():
    """Регистрируем handlers для 'Текущие акции'"""
    dp.register_message_handler(current_promotions_handler)