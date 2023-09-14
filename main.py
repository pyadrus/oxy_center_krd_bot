from aiogram import executor
from loguru import logger

from handlers.ask_anonymous_question_handlers import register_ask_anonymous_question_handler
from handlers.contacts_and_address_handlers import register_contacts_and_address_handler
from handlers.current_promotions_handlers import register_current_promotions_handler
from handlers.sign_up_handlers import register_callback_query_handler
from handlers.user_handlers import greeting_handler
from system.dispatcher import dp

logger.add("logs/log.log", retention="1 days", enqueue=True)  # Логирование бота


def main() -> None:
    """Запуск бота https://t.me/oxy_center_krd_bot"""
    try:
        executor.start_polling(dp, skip_updates=True)
    except Exception as e:
        logger.exception(e)

    greeting_handler()  # Пост приветствие
    register_current_promotions_handler()  # Текущие акции
    register_contacts_and_address_handler()  # Контакты и адрес
    register_ask_anonymous_question_handler()  # Задать анонимный вопрос
    register_callback_query_handler() # Записаться


if __name__ == '__main__':
    try:
        main()  # Запуск бота
    except Exception as e:
        logger.exception(e)
