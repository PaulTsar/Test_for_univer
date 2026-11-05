from database_sqlite import get_connection
from models.attendance import Attendance

def _map(row) -> Attendance:
    return Attendance(
        attendance_id=row[0],
        lesson_id=row[1],
        student_id=row[2],
        status=row[3],
        student_name=row[4] if len(row) > 4 else None,
        lesson_date=row[5] if len(row) > 5 else None
    )

def create(lesson_id: int, student_id: int, status: str = 'absent') -> int:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO attendance (lesson_id, student_id, status) 
        VALUES (?, ?, ?)
    """, (lesson_id, student_id, status))
    conn.commit()
    new_id = cur.lastrowid
    conn.close()
    return new_id

def get_by_lesson(lesson_id: int) -> list[Attendance]:
    """Возвращает всех студентов группы и их отметки для конкретного занятия."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT a.attendance_id, a.lesson_id, a.student_id, a.status, s.full_name, l.date
        FROM attendance a
        JOIN students s ON s.student_id = a.student_id
        JOIN lessons l ON l.lesson_id = a.lesson_id
        WHERE a.lesson_id = ?
    """, (lesson_id,))
    rows = cur.fetchall()
    conn.close()
    return [_map(r) for r in rows]

def get_by_student(student_id: int) -> list[Attendance]:
    """Возвращает всю посещаемость конкретного студента."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT a.attendance_id, a.lesson_id, a.student_id, a.status, l.date
        FROM attendance a
        JOIN lessons l ON l.lesson_id = a.lesson_id
        WHERE a.student_id = ?
        ORDER BY l.date DESC
    """, (student_id,))
    rows = cur.fetchall()
    conn.close()
    return [_map(r) for r in rows]

def update_status(attendance_id: int, status: str) -> None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE attendance SET status = ? WHERE attendance_id = ?", (status, attendance_id))
    conn.commit()
    conn.close()

def delete(attendance_id: int) -> None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM attendance WHERE attendance_id = ?", (attendance_id,))
    conn.commit()
    conn.close()