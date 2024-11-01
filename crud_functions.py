import sqlite3 as sql

connection = sql.connect('database.db')
cursor = connection.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products(
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        price INT NOT NULL
    );
''')

cursor.execute("DELETE FROM Products")
for i in range(1, 5):
    cursor.execute("INSERT INTO Products (title, description, price) VALUES (?, ?, ?)",
                   (f'Продукт {i}', f'Описание {i}', i * 100))
    connection.commit()


cursor.execute("DELETE FROM Users")
for i in range(1, 11):
    cursor.execute("INSERT INTO Users (username, email, age, balance) VALUES (?, ?, ?, ?)",
                   (f'Name {i}', f'X{i}@gmail.com', i * 7, 1000))
    connection.commit()


def get_all_products():
    return cursor.execute("SELECT * FROM Products")


def initiate_db():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users(
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            email TEXT NOT NULL,
            age INT NOT NULL,
            balance INT NOT NULL
        );
    ''')


def is_included(username):
    cursor.execute("SELECT 1 FROM Users WHERE username = ? LIMIT 1", (username,))
    if cursor.fetchone() is not None:
        return True
    else:
        return False


def add_user(username, email, age):
    if not is_included(username):
        cursor.execute("INSERT INTO Users (username, email, age, balance) VALUES (?,?,?,?)",
                       (username, email, age, 1000))
        connection.commit()


connection.commit()
