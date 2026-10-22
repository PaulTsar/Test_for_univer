import sqlite3
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parent.parent
DB_PATH = PROJECT_DIR / 'data' / 'attendance_lab3.db'


def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DB_PATH)
    connection.execute('PRAGMA foreign_keys = ON')
    return connection
