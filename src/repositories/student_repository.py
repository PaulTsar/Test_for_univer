from __future__ import annotations
from database_sqlite import get_connection
from models.student import Student

def _map(row) -> Student:
    return Student(*row)

def create(full_name: str, group_id: int) -> int:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO students (full_name, group_id) VALUES (?, ?)", (full_name, group_id))
    conn.commit()
    new_id = cur.lastrowid
    conn.close()
    return new_id

def get_by_id(student_id: int) -> Student | None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT s.student_id, s.full_name, s.group_id, g.name AS group_name
        FROM students s
        JOIN "groups" g ON g.group_id = s.group_id
        WHERE s.student_id = ?
    """, (student_id,))
    row = cur.fetchone()
    conn.close()
    return _map(row) if row else None

def get_all() -> list[Student]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT s.student_id, s.full_name, s.group_id, g.name AS group_name
        FROM students s
        JOIN "groups" g ON g.group_id = s.group_id
        ORDER BY s.full_name
    """)
    rows = cur.fetchall()
    conn.close()
    return [_map(r) for r in rows]

def update(student_id: int, full_name: str, group_id: int) -> None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE students SET full_name = ?, group_id = ? WHERE student_id = ?", (full_name, group_id, student_id))
    conn.commit()
    conn.close()

def delete(student_id: int) -> None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM students WHERE student_id = ?", (student_id,))
    conn.commit()
    conn.close()