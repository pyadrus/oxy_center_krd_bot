import sqlite3


def writing_to_the_database(surname, name, phone):
    """Запись данных в базу данных"""
    conn = sqlite3.connect('your_database.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS orders 
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, surname TEXT, name TEXT, phone TEXT)''')
    cursor.execute("INSERT INTO orders (surname, name, phone) VALUES (?, ?, ?)", (surname, name, phone))
    conn.commit()
    conn.close()


def get_user_data_from_db(user_id):
    conn = sqlite3.connect("your_database.db")  # Замените "your_database.db" на имя вашей базы данных
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (user_id INTEGER,
                                                        name TEXT,
                                                        surname TEXT,
                                                        city TEXT,
                                                        phone_number TEXT,
                                                        registration_date TEXT)''')
    # Выполните SQL-запрос для получения данных о пользователе по его user_id
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    user_data = cursor.fetchone()  # Получите данные первой найденной записи
    conn.close()
    # Верните данные о пользователе как словарь, если они существуют, или None, если пользователя нет
    if user_data:
        _, name, surname, city, phone_number, registration_date = user_data
        return {'name': name, 'surname': surname, 'city': city, 'phone_number': phone_number,
                'registration_date': registration_date}
    else:
        return None


# Функция для изменения имени в базе данных по ID
def update_name_in_db(user_id, new_name):
    try:
        # Подключаемся к базе данных (предполагается, что она уже существует)
        conn = sqlite3.connect('your_database.db')
        cursor = conn.cursor()
        # SQL-запрос для обновления имени
        update_query = "UPDATE users SET name = ? WHERE user_id = ?"
        cursor.execute(update_query, (new_name, user_id))
        conn.commit()  # Применяем изменения к базе данных
        conn.close()  # Закрываем соединение с базой данных
        return True  # Возвращаем True в случае успешного обновления
    except Exception as e:
        print("Ошибка при обновлении имени:", str(e))
        return False  # Возвращаем False в случае ошибки


def update_surname_in_db(user_id, new_surname):
    try:
        # Подключаемся к базе данных (предполагается, что она уже существует)
        conn = sqlite3.connect('your_database.db')
        cursor = conn.cursor()
        # SQL-запрос для обновления имени
        update_query = "UPDATE users SET surname = ? WHERE user_id = ?"
        cursor.execute(update_query, (new_surname, user_id))
        conn.commit()  # Применяем изменения к базе данных
        conn.close()  # Закрываем соединение с базой данных
        return True  # Возвращаем True в случае успешного обновления
    except Exception as e:
        print("Ошибка при обновлении фамилии:", str(e))
        return False  # Возвращаем False в случае ошибки


def update_city_in_db(user_id, new_city):
    try:
        # Подключаемся к базе данных (предполагается, что она уже существует)
        conn = sqlite3.connect('your_database.db')
        cursor = conn.cursor()
        # SQL-запрос для обновления имени
        update_query = "UPDATE users SET city = ? WHERE user_id = ?"
        cursor.execute(update_query, (new_city, user_id))
        conn.commit()  # Применяем изменения к базе данных
        conn.close()  # Закрываем соединение с базой данных
        return True  # Возвращаем True в случае успешного обновления
    except Exception as e:
        print("Ошибка при обновлении фамилии:", str(e))
        return False  # Возвращаем False в случае ошибки


def update_phone_in_db(user_id, new_phone):
    try:
        # Подключаемся к базе данных (предполагается, что она уже существует)
        conn = sqlite3.connect('your_database.db')
        cursor = conn.cursor()
        # SQL-запрос для обновления имени
        update_query = "UPDATE users SET phone_number = ? WHERE user_id = ?"
        cursor.execute(update_query, (new_phone, user_id))
        conn.commit()  # Применяем изменения к базе данных
        conn.close()  # Закрываем соединение с базой данных
        return True  # Возвращаем True в случае успешного обновления
    except Exception as e:
        print("Ошибка при обновлении фамилии:", str(e))
        return False  # Возвращаем False в случае ошибки
