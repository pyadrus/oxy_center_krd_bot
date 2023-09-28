from aiogram import executor
from loguru import logger

from handlers.admin_handlers.admin_headlers import send_data_as_excel_handler
from handlers.user_handlers.ask_anonymous_question_handlers import register_ask_anonymous_question_handler
from handlers.user_handlers.contacts_and_address_handlers import register_contacts_and_address_handler
from handlers.user_handlers.current_promotions_handlers import register_current_promotions_handler
from handlers.user_handlers.leave_review_handlers import register_leave_review_handler
from handlers.user_handlers.my_details_handlers import register_my_details_handler
from handlers.user_handlers.sign_up_handlers import register_callback_query_handler
from handlers.user_handlers.user_handlers import greeting_handler
from system.dispatcher import dp

logger.add("logs/log.log", retention="1 days", enqueue=True)  # Логирование бота


def main() -> None:
    """Запуск бота https://t.me/oxy_center_krd_bot"""
    try:
        executor.start_polling(dp, skip_updates=True)
    except Exception as error:
        logger.exception(error)

    greeting_handler()  # Пост приветствие
    register_current_promotions_handler()  # Текущие акции
    register_contacts_and_address_handler()  # Контакты и адрес
    register_ask_anonymous_question_handler()  # Задать анонимный вопрос
    register_callback_query_handler()  # Записаться
    register_my_details_handler()  # Мои данные
    send_data_as_excel_handler()
    register_leave_review_handler() # Оставить отзыв


if __name__ == '__main__':
    try:
        main()  # Запуск бота
    except Exception as e:
        logger.exception(e)
