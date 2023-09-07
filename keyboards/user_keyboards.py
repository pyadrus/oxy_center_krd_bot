from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def greeting_keyboards():
    """Клавиатуры поста приветствия 👋"""
    keyboards_greeting = InlineKeyboardMarkup()
    ask_anonymous_question = InlineKeyboardButton(text='Задать анонимный вопрос',
                                                  callback_data='ask_anonymous_question')
    sign_up = InlineKeyboardButton(text='Записаться',
                                   callback_data='sign_up')
    contacts_and_address = InlineKeyboardButton(text='Контакты и адрес',
                                                callback_data='contacts_and_address')
    contact_the_operator = InlineKeyboardButton(text='Связаться с оператором',
                                                callback_data='contact_the_operator')
    current_promotions = InlineKeyboardButton(text='Текущие акции',
                                              callback_data='current_promotions')

    keyboards_greeting.row(ask_anonymous_question)  # Задать анонимный вопрос
    keyboards_greeting.row(sign_up)  # Записаться
    keyboards_greeting.row(contacts_and_address, current_promotions)  # Контакты и адрес, Текущие акции
    keyboards_greeting.row(contact_the_operator)  # Связаться с оператором
    return keyboards_greeting


if __name__ == '__main__':
    greeting_keyboards()
