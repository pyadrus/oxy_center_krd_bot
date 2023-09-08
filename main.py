from aiogram import executor
from loguru import logger
from handlers.contacts_and_address_handlers import register_contacts_and_address_handler
from handlers.current_promotions_handlers import register_current_promotions_handler
from handlers.user_handlers import greeting_handler
from system.dispatcher import dp

logger.add("logs/log.log", retention="1 days", enqueue=True)  # Логирование бота


def main() -> None:
    """Запуск бота https://t.me/oxy_center_krd_bot"""
    executor.start_polling(dp, skip_updates=True)
    greeting_handler()
    register_current_promotions_handler()  # Текущие акции
    register_contacts_and_address_handler()  # Контакты и адрес


if __name__ == '__main__':
    try:
        main()  # Запуск бота
    except Exception as e:
        logger.exception(e)
