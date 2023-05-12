"""
all database functions in here
"""
import sqlite3
from config import DATABASE_NAME


def create_days_table():
    """
    DATABASE-so'zi bilan yangi bog'lanish ochib, days jadvalini yaratadi.
    qatorlari name o'zgaruvchisi (1 text)
    """
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS days (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT
            );
        """)


def create_media_types_table():
    """
    DATABASE-so'zi bilan yangi bog'lanish ochib, media_types jadvalini yaratadi.
    qatorlari name o'zgaruvchisi (1 text) va days_id (1 foreign key)
    """
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS media_types (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                days_id INTEGER,
                FOREIGN KEY (days_id) REFERENCES days (id)
            );
        """)


def create_media_table():
    """
    DATABASE-so'zi bilan yangi bog'lanish ochib, media jadvalini yaratadi.
    qatorlari media_types_id (1 foreign key) va media_id (1 text)
    """
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS media (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                media_types_id INTEGER,
                media_id TEXT,
                FOREIGN KEY (media_types_id) REFERENCES media_types (id)
            );
        """)


def create_users_table():
    """
    Establishes a connection to the DATABASE_NAME and creates the users table if it doesn't exist.
    The table has columns for user_id (INTEGER PRIMARY KEY) and username (TEXT).
    """
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT
            );
        """)


def add_user(user_id, username):
    """
    Establishes a connection to the DATABASE_NAME and inserts a new user into the users table.
    user_id - Telegram user ID (INTEGER)
    username - Telegram username (TEXT)
    """
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (user_id, username) VALUES (?, ?)", (user_id, username))
        conn.commit()


def get_all_users():
    """
    Establishes a connection to the DATABASE_NAME and retrieves all users from the users table.
    Returns the data as a list of tuples containing (user_id, username).
    """
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        return rows


def get_users_count():
    """
    Establishes a connection to the DATABASE_NAME and retrieves the count of users from the users table.
    Returns the number of users (integer).
    """
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM users")
        count = cursor.fetchone()[0]
        return count


def create_database():
    """
    create database
    :return:
    """
    create_users_table()
    create_days_table()
    create_media_table()
    create_media_types_table()


def insert_day(name):
    """
    DATABASE-so'zi bilan yangi bog'lanish ochib, days jadvaliga yangi qator qo'shadi
    name - yangi qatorning nomi (text)
    """
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO days (name) VALUES (?)", (name,))
        conn.commit()


def insert_media_type(name, day):
    """
    DATABASE-so'zi bilan yangi bog'lanish ochib, media_types jadvaliga yangi qator qo'shadi
    name - yangi qatorning nomi (text)
    days_id - foreign key days jadvalidagi id sifatida beriladi
    """
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor_day = conn.cursor()
        cursor = conn.cursor()
        cursor_day.execute("SELECT id FROM days WHERE name=?", (day, ))
        days_id = cursor_day.fetchone()
        cursor.execute("INSERT INTO media_types (name, days_id) VALUES (?, ?)", (name, days_id[0],))
        conn.commit()


def insert_media(media_type, media_id, day):
    """
    DATABASE-so'zi bilan yangi bog'lanish ochib, media jadvaliga yangi qator qo'shadi
    media_types_id - foreign key media_types jadvalidagi id sifatida beriladi
    media_id - yangi qatorning media_id (text)
    """
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor_day = conn.cursor()
        cursor_day.execute("SELECT id FROM days WHERE name=?", (day, ))
        days_id = cursor_day.fetchone()[0]
        cursor_media_type = conn.cursor()
        cursor_media_type.execute("SELECT id FROM media_types WHERE name=? AND days_id=?", (media_type, days_id))
        media_types_id = cursor_media_type.fetchone()[0]
        cursor.execute("INSERT INTO media (media_types_id, media_id) VALUES (?, ?)", (media_types_id, media_id,))
        conn.commit()


def read_media_types(days_id):
    """
    Establishes a connection to the DATABASE_NAME and retrieves all data from the media table
    for the specified days_id.
    Returns the data as a list of tuples.
    """
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM media_types WHERE days_id=?", (days_id,))
        rows = cursor.fetchall()
        return rows


def read_days():
    """
    Establishes a connection to the DATABASE_NAME and retrieves all data from the days table.
    Returns the data as a list of tuples.
    """
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM days")
        rows = cursor.fetchall()
        return rows


def read_media(media_type, day):
    """
    Establishes a connection to the DATABASE_NAME and retrieves all data from the media table
    for the specified days_id.
    Returns the data as a list of tuples.
    """
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor_day = conn.cursor()
        cursor_day.execute("SELECT id FROM days WHERE name=?", (day, ))
        days_id = cursor_day.fetchone()[0]
        cursor_media_type = conn.cursor()
        cursor_media_type.execute("SELECT id FROM media_types WHERE name=? AND days_id=?", (media_type, days_id))
        media_types_id = cursor_media_type.fetchone()[0]
        cursor.execute("SELECT * FROM media WHERE media_types_id=?", (media_types_id,))
        rows = cursor.fetchall()
        return rows


def delete_media_type(media_type, day):
    """
    Establishes a connection to the DATABASE_NAME and deletes the row from the media_types table with the specified
    media_type_id.
    media_type_id - the id of the row to be deleted
    """
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor_day = conn.cursor()
        cursor_day.execute("SELECT id FROM days WHERE name=?", (day, ))
        days_id = cursor_day.fetchone()[0]
        cursor_media_type = conn.cursor()
        cursor_media_type.execute("SELECT id FROM media_types WHERE name=? AND days_id=?", (media_type, days_id))
        media_types_id = cursor_media_type.fetchone()[0]
        cursor.execute("DELETE FROM media_types WHERE id=?", (media_types_id,))
        conn.commit()


def delete_media(media_name):
    """
    Establishes a connection to the DATABASE_NAME and deletes the row from the media table with the specified media_id.
    media_id - the id of the row to be deleted
    """
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM media WHERE media_id=?", (media_name,))
        conn.commit()


def delete_day(day):
    """
    Establishes a connection to the DATABASE_NAME and deletes the row from the days table with the specified day_id.
    day_id - the id of the row to be deleted
    """
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM days WHERE name=?", (day,))
        conn.commit()
