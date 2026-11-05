from __future__ import annotations
from database_sqlite import get_connection
from models.group import Group

def _map(row) -> Group:
    return Group(*row)

def create(name: str) -> int:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO groups (name) VALUES (?)", (name,))
    conn.commit()
    new_id = cur.lastrowid
    conn.close()
    return new_id

def get_by_id(group_id: int) -> Group | None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT group_id, name FROM groups WHERE group_id = ?", (group_id,))
    row = cur.fetchone()
    conn.close()
    return _map(row) if row else None

def get_all() -> list[Group]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT group_id, name FROM groups ORDER BY name")
    rows = cur.fetchall()
    conn.close()
    return [_map(r) for r in rows]

def update(group_id: int, name: str) -> None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE groups SET name = ? WHERE group_id = ?", (name, group_id))
    conn.commit()
    conn.close()

def delete(group_id: int) -> None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM groups WHERE group_id = ?", (group_id,))
    conn.commit()
    conn.close()