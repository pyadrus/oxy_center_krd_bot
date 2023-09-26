from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton


def greeting_keyboards():
    """Клавиатуры поста приветствия 👋"""
    keyboards_greeting = InlineKeyboardMarkup()
    ask_anonymous_question = InlineKeyboardButton(text='🕵️ Задать анонимный вопрос',
                                                  callback_data='ask_anonymous_question')
    sign_up = InlineKeyboardButton(text='📝 Записаться',
                                   callback_data='sign_up')
    contacts_and_address = InlineKeyboardButton(text='📞 Контакты и адрес',
                                                callback_data='contacts_and_address')
    contact_the_operator = InlineKeyboardButton(text='👷 Связаться с оператором', url="https://t.me/pk_alina")
    current_promotions = InlineKeyboardButton(text='🎉 Текущие акции',
                                              callback_data='current_promotions')
    my_details = InlineKeyboardButton(text='Мои данные', callback_data='my_details')
    keyboards_greeting.row(ask_anonymous_question)  # Задать анонимный вопрос
    keyboards_greeting.row(sign_up)  # Записаться
    keyboards_greeting.row(contacts_and_address, current_promotions)  # Контакты и адрес, Текущие акции
    keyboards_greeting.row(contact_the_operator)  # Связаться с оператором
    keyboards_greeting.row(my_details)  # Связаться с оператором
    return keyboards_greeting


def my_details():
    """Кнопка мои данные"""
    my_details_key = InlineKeyboardMarkup()
    my_detailss = InlineKeyboardButton(text='Мои данные', callback_data='my_details')
    my_details_key.row(my_detailss)  # Связаться с оператором
    return my_details_key


def sign_up_keyboards():
    """
    👍 Согласен - agree
    👎 Не согласен - disagree
    """
    keyboards_sign_up = InlineKeyboardMarkup()
    agree = InlineKeyboardButton(text='👍 Согласен', callback_data='agree')
    after = InlineKeyboardButton(text='👎 Не согласен', callback_data='disagree')
    keyboards_sign_up.row(agree, after)
    return keyboards_sign_up


def confirmation_keypad():
    """
    👍 Верно - faithfully
    👎 Не верно - not_true
    """
    confirmation_keyboards = InlineKeyboardMarkup()
    faithfully = InlineKeyboardButton(text="👍 Верно", callback_data="faithfully")
    not_true = InlineKeyboardButton(text="👎 Не верно", callback_data="not_true")
    confirmation_keyboards.row(faithfully, not_true)
    return confirmation_keyboards


def appointment_selection_keypad():
    """
    Позвонить - сall_key
    Заказать обратный звонок - callback_key
    Чат с оператором - url="https://t.me/pk_alina"
    """
    appointment_selection_key = InlineKeyboardMarkup()
    call_key = InlineKeyboardButton(text="Позвонить", callback_data="call_us")
    callback_key = InlineKeyboardButton(text="Заказать обратный звонок", callback_data="callback_key")
    chat_with_an_operator_key = InlineKeyboardButton(text="Чат с оператором", url="https://t.me/pk_alina")
    appointment_selection_key.row(call_key, callback_key)
    appointment_selection_key.row(chat_with_an_operator_key)
    return appointment_selection_key


def contact_keyboard():
    """Клавиатура отправки отчетов"""
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    # Add a button for sending the contact
    send_contact_button = KeyboardButton("📱 Отправить", request_contact=True)
    # Add a button for manual input
    manual_input_button = KeyboardButton("📝 Ввести вручную")
    markup.add(send_contact_button)
    markup.add(manual_input_button)
    return markup


def data_modification_keyboard():
    """Клавиатура изменения данных"""
    # Создаем клавиатуру для редактирования данных
    edit_data_keyboard = InlineKeyboardMarkup()
    edit_name_button = InlineKeyboardButton("Изменить Имя", callback_data="edit_name")
    edit_surname_button = InlineKeyboardButton("Изменить Фамилию", callback_data="edit_surname")
    edit_city_button = InlineKeyboardButton("Изменить Город", callback_data="edit_city")
    edit_phone_button = InlineKeyboardButton("Изменить Номер 📱 ", callback_data="edit_phone")

    edit_data_keyboard.row(edit_name_button, edit_surname_button)
    edit_data_keyboard.row(edit_city_button, edit_phone_button)
    return edit_data_keyboard


if __name__ == '__main__':
    greeting_keyboards()
    sign_up_keyboards()
    confirmation_keypad()
    appointment_selection_keypad()
    contact_keyboard()
    my_details()
