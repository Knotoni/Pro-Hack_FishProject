import sqlite3
import traceback

DB_PATH = 'data/database.db'

def execute(query: str):
    try:
        sqlite_connection = sqlite3.connect(DB_PATH)
        cursor = sqlite_connection.cursor()
        cursor.execute(query)
        record = cursor.fetchall()
        if bool(record):
            return record
        else:
            return None
    except Exception as ex:
        traceback.print_exc()

def find_user(user_name: str):
    data = execute(f"SELECT id FROM users WHERE login = '{user_name}'")
    return bool(data)

def check_password(user_name: str, password: str):
    data = execute(f"SELECT id FROM users WHERE login = '{user_name}' AND password_hash = '{password}'")
    return bool(data)

