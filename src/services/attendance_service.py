from __future__ import annotations

from models.user import User
from models.attendance import Attendance
from repositories import attendance_repository, lesson_repository, student_repository


def mark_attendance(teacher: User, lesson_id: int, student_id: int, status: str) -> None:
    """
    Отмечает посещаемость студента на занятии.
    Проверяет: ведет ли этот преподаватель занятие, и учится ли студент в нужной группе.
    """
    if status not in ('present', 'absent', 'excused'):
        raise Exception("Недопустимый статус посещаемости")

    lesson = lesson_repository.get_by_id(lesson_id)
    if not lesson:
        raise Exception("Занятие не найдено")

    if lesson.teacher_id != teacher.teacher_id:
        raise Exception("Вы не можете отмечать посещаемость на чужом занятии")

    student = student_repository.get_by_id(student_id)
    if not student:
        raise Exception("Студент не найден")

    if student.group_id != lesson.group_id:
        raise Exception("Студент не относится к группе этого занятия")

    existing_attendances = attendance_repository.get_by_lesson(lesson_id)
    for att in existing_attendances:
        if att.student_id == student_id:
            attendance_repository.update_status(att.attendance_id, status)
            return

    attendance_repository.create(lesson_id, student_id, status)


def get_student_attendance(student_id: int) -> list[Attendance]:
    """Возвращает список посещаемости для конкретного студента."""
    return attendance_repository.get_by_student(student_id)


def get_lesson_attendance(teacher: User, lesson_id: int) -> list[Attendance]:
    """Возвращает посещаемость занятия (только для преподавателя этого занятия)."""
    lesson = lesson_repository.get_by_id(lesson_id)
    if not lesson:
        raise Exception("Занятие не найдено")
    if lesson.teacher_id != teacher.teacher_id:
        raise Exception("Вы не можете просматривать чужое занятие")

    return attendance_repository.get_by_lesson(lesson_id)