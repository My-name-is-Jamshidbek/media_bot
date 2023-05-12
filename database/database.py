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


def create_database():
    """
    create database
    :return:
    """
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


def insert_media_type(name, days_id):
    """
    DATABASE-so'zi bilan yangi bog'lanish ochib, media_types jadvaliga yangi qator qo'shadi
    name - yangi qatorning nomi (text)
    days_id - foreign key days jadvalidagi id sifatida beriladi
    """
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO media_types (name, days_id) VALUES (?, ?)", (name, days_id,))
        conn.commit()


def insert_media(media_types_id, media_id):
    """
    DATABASE-so'zi bilan yangi bog'lanish ochib, media jadvaliga yangi qator qo'shadi
    media_types_id - foreign key media_types jadvalidagi id sifatida beriladi
    media_id - yangi qatorning media_id (text)
    """
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
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


def read_media(media_types_id):
    """
    Establishes a connection to the DATABASE_NAME and retrieves all data from the media table
    for the specified days_id.
    Returns the data as a list of tuples.
    """
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM media WHERE media_types_id=?", (media_types_id,))
        rows = cursor.fetchall()
        return rows


def delete_media_type(media_type_id):
    """
    Establishes a connection to the DATABASE_NAME and deletes the row from the media_types table with the specified media_type_id.
    media_type_id - the id of the row to be deleted
    """
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM media_types WHERE id=?", (media_type_id,))
        conn.commit()


def delete_media(media_id):
    """
    Establishes a connection to the DATABASE_NAME and deletes the row from the media table with the specified media_id.
    media_id - the id of the row to be deleted
    """
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM media WHERE id=?", (media_id,))
        conn.commit()


def delete_day(day_id):
    """
    Establishes a connection to the DATABASE_NAME and deletes the row from the days table with the specified day_id.
    day_id - the id of the row to be deleted
    """
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM days WHERE id=?", (day_id,))
        conn.commit()
