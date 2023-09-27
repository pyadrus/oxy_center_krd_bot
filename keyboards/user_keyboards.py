from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton


def create_greeting_keyboard():
    """Создает клавиатуру для приветственного сообщения 👋"""
    greeting_keyboard = InlineKeyboardMarkup()
    ask_anonymous_question_button = InlineKeyboardButton(text='🕵️ Задать анонимный вопрос',
                                                         callback_data='ask_anonymous_question')
    sign_up_button = InlineKeyboardButton(text='📝 Записаться',
                                          callback_data='sign_up')
    contacts_and_address_button = InlineKeyboardButton(text='📞 Контакты и адрес',
                                                       callback_data='contacts_and_address')
    contact_operator_button = InlineKeyboardButton(text='👷 Связаться с оператором', url="https://t.me/pk_alina")
    current_promotions_button = InlineKeyboardButton(text='🎉 Текущие акции',
                                                     callback_data='current_promotions')
    my_details_button = InlineKeyboardButton(text='Мои данные', callback_data='my_details')

    greeting_keyboard.row(ask_anonymous_question_button)  # Задать анонимный вопрос
    greeting_keyboard.row(sign_up_button)  # Записаться
    greeting_keyboard.row(contacts_and_address_button, current_promotions_button)  # Контакты и адрес, Текущие акции
    greeting_keyboard.row(contact_operator_button)  # Связаться с оператором
    greeting_keyboard.row(my_details_button)  # Связаться с оператором
    return greeting_keyboard


def create_my_details_keyboard():
    """Создает клавиатуру для кнопки 'Мои данные'"""
    my_details_keyboard = InlineKeyboardMarkup()
    my_details_button = InlineKeyboardButton(text='Мои данные', callback_data='my_details')

    my_details_keyboard.row(my_details_button)  # Связаться с оператором
    return my_details_keyboard


def create_sign_up_keyboard():
    """Создает клавиатуру для кнопок 'Согласен' и 'Не согласен'"""
    sign_up_keyboard = InlineKeyboardMarkup()
    agree_button = InlineKeyboardButton(text='👍 Согласен', callback_data='agree')
    disagree_button = InlineKeyboardButton(text='👎 Не согласен', callback_data='disagree')

    sign_up_keyboard.row(agree_button, disagree_button)
    return sign_up_keyboard


def appointment_selection_keypad():
    """Создает клавиатуру для выбора способа связи"""
    appointment_selection_key = InlineKeyboardMarkup()
    call_button = InlineKeyboardButton(text="Позвонить", callback_data="call_us")
    callback_button = InlineKeyboardButton(text="Заказать обратный звонок", callback_data="callback_key")
    chat_with_operator_button = InlineKeyboardButton(text="Чат с оператором", url="https://t.me/pk_alina")

    appointment_selection_key.row(call_button, callback_button)
    appointment_selection_key.row(chat_with_operator_button)
    return appointment_selection_key


def create_contact_keyboard():
    """Создает клавиатуру для отправки контакта"""
    contact_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    send_contact_button = KeyboardButton("📱 Отправить", request_contact=True)

    contact_keyboard.add(send_contact_button)
    return contact_keyboard


def create_data_modification_keyboard():
    """Создает клавиатуру для изменения данных"""
    data_modification_keyboard = InlineKeyboardMarkup()
    edit_name_button = InlineKeyboardButton("✏️Изменить Имя", callback_data="edit_name")
    edit_surname_button = InlineKeyboardButton("✏️Изменить Фамилию", callback_data="edit_surname")
    edit_city_button = InlineKeyboardButton("✏️Изменить Город", callback_data="edit_city")
    edit_phone_button = InlineKeyboardButton("✏️Изменить Номер 📱 ", callback_data="edit_phone")

    data_modification_keyboard.row(edit_name_button, edit_surname_button)
    data_modification_keyboard.row(edit_city_button, edit_phone_button)
    return data_modification_keyboard


if __name__ == '__main__':
    create_greeting_keyboard()
    create_sign_up_keyboard()
    appointment_selection_keypad()
    create_contact_keyboard()
    create_my_details_keyboard()
    create_data_modification_keyboard()
