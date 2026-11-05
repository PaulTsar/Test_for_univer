from __future__ import annotations
from database_sqlite import get_connection
from models.teacher import Teacher

def _map(row) -> Teacher:
    return Teacher(*row)

def create(full_name: str) -> int:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO teachers (full_name) VALUES (?)", (full_name,))
    conn.commit()
    new_id = cur.lastrowid
    conn.close()
    return new_id

def get_by_id(teacher_id: int) -> Teacher | None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT teacher_id, full_name FROM teachers WHERE teacher_id = ?", (teacher_id,))
    row = cur.fetchone()
    conn.close()
    return _map(row) if row else None

def get_all() -> list[Teacher]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT teacher_id, full_name FROM teachers ORDER BY full_name")
    rows = cur.fetchall()
    conn.close()
    return [_map(r) for r in rows]