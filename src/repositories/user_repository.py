from __future__ import annotations
from database_sqlite import get_connection
from models.user import User

def _map(row) -> User:
    return User(*row)

def get_by_login(login: str) -> User | None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT user_id, login, password_hash, role, student_id, teacher_id
        FROM users WHERE login = ?
    """, (login,))
    row = cur.fetchone()
    conn.close()
    return _map(row) if row else None

def get_by_id(user_id: int) -> User | None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT user_id, login, password_hash, role, student_id, teacher_id
        FROM users WHERE user_id = ?
    """, (user_id,))
    row = cur.fetchone()
    conn.close()
    return _map(row) if row else None