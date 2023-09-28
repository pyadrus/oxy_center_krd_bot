from aiogram import types
from loguru import logger

from keyboards.user_keyboards import stock_keyboard
from messages.user_messages import current_promotions_text, happy_parents_text, \
    the_second_opinion_of_the_operators_text, second_opinion_of_fertility_specialists_text
from system.dispatcher import dp, bot


@dp.callback_query_handler(lambda c: c.data == 'current_promotions')
async def current_promotions_handler(callback_query: types.CallbackQuery):
    """Текущие акции"""
    try:
        stock_keyboards = stock_keyboard()
        await bot.send_message(callback_query.from_user.id, current_promotions_text,
                               reply_markup=stock_keyboards,
                               parse_mode=types.ParseMode.HTML)
    except Exception as error:
        logger.exception(error)


@dp.callback_query_handler(lambda c: c.data == 'happy_parents')
async def happy_parents_handler(callback_query: types.CallbackQuery):
    """Счастливые родители"""
    try:
        await bot.send_message(callback_query.from_user.id, happy_parents_text,
                               parse_mode=types.ParseMode.HTML)
    except Exception as error:
        logger.exception(error)


@dp.callback_query_handler(lambda c: c.data == 'second_opinion_of_fertility_specialists')
async def second_opinion_of_fertility_specialists_handler(callback_query: types.CallbackQuery):
    """Второе мнение репродуктологов БЕСПАЛТНО"""
    try:
        await bot.send_message(callback_query.from_user.id, second_opinion_of_fertility_specialists_text,
                               parse_mode=types.ParseMode.HTML)
    except Exception as error:
        logger.exception(error)


@dp.callback_query_handler(lambda c: c.data == 'the_second_opinion_of_the_operators')
async def the_second_opinion_of_the_operators_handler(callback_query: types.CallbackQuery):
    """Второе мнение оперирующих гинекологов БЕСПЛАТНО"""
    try:
        await bot.send_message(callback_query.from_user.id, the_second_opinion_of_the_operators_text,
                               parse_mode=types.ParseMode.HTML)
    except Exception as error:
        logger.exception(error)


def register_current_promotions_handler():
    """Регистрируем handlers для 'Текущие акции'"""
    dp.register_message_handler(current_promotions_handler)
    dp.register_message_handler(second_opinion_of_fertility_specialists_handler)
    dp.register_message_handler(happy_parents_handler)
    dp.register_message_handler(the_second_opinion_of_the_operators_handler)
