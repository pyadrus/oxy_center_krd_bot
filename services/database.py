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

