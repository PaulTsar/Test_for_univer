from __future__ import annotations
from database_sqlite import get_connection
from models.lesson import Lesson

def _map(row) -> Lesson:
    return Lesson(*row)

def create(date: str, group_id: int, teacher_id: int) -> int:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO lessons (date, group_id, teacher_id) VALUES (?, ?, ?)", (date, group_id, teacher_id))
    conn.commit()
    new_id = cur.lastrowid
    conn.close()
    return new_id

def get_by_id(lesson_id: int) -> Lesson | None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT l.lesson_id, l.date, l.group_id, l.teacher_id, g.name AS group_name, t.full_name AS teacher_name
        FROM lessons l
        JOIN "groups" g ON g.group_id = l.group_id
        JOIN teachers t ON t.teacher_id = l.teacher_id
        WHERE l.lesson_id = ?
    """, (lesson_id,))
    row = cur.fetchone()
    conn.close()
    return _map(row) if row else None

def get_all() -> list[Lesson]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT l.lesson_id, l.date, l.group_id, l.teacher_id, g.name AS group_name, t.full_name AS teacher_name
        FROM lessons l
        JOIN "groups" g ON g.group_id = l.group_id
        JOIN teachers t ON t.teacher_id = l.teacher_id
        ORDER BY l.date DESC
    """)
    rows = cur.fetchall()
    conn.close()
    return [_map(r) for r in rows]