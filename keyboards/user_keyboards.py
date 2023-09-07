from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def greeting_keyboards():
    """Клавиатуры поста приветствия 👋"""
    keyboards_greeting = InlineKeyboardMarkup()
    get_a_bonus = InlineKeyboardButton(text='📥 Первая кнопка', callback_data='one_key')
    reference_keyboard = InlineKeyboardButton(text='📤 Вторая кнопка', callback_data='tv_key')
    keyboards_greeting.row(get_a_bonus)
    keyboards_greeting.row(reference_keyboard)
    return keyboards_greeting


if __name__ == '__main__':
    greeting_keyboards()