import sqlite3
connection = sqlite3.connect('initiate_db.db')
cursor = connection.cursor()

cursor.execute("DROP TABLE IF EXISTS Products")

cursor.execute('''
CREATE TABLE IF NOT EXISTS Products(
id INTEGER PRIMARY KEY AUTOINCREMENT,
title TEXT NOT NULL,
description TEXT,
price INTEGER NOT NULL
)
''')

for i in range(1, 5):
    cursor.execute("INSERT INTO Products (title, description, price) VALUES (?, ?, ?)", (f'Продукт {i}', f'Описание {i}', i * 100))

def get_all_products():
    cursor.execute("SELECT * FROM Products")
    return cursor.fetchall()


connection.commit()
connection.close()