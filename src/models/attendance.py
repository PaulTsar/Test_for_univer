from __future__ import annotations
from dataclasses import dataclass


STATUS_NAMES = {
    "present": "Присутствовал",
    "absent": "Отсутствовал",
    "excused": "Уважительная причина",
}


@dataclass
class Attendance:
    attendance_id: int | None = None
    lesson_id: int | None = None
    student_id: int | None = None
    status: str = "absent"

    status_name: str | None = None
    student_name: str | None = None
    lesson_date: str | None = None
    group_name: str | None = None

    def __post_init__(self):
        if self.status_name is None:
            self.status_name = STATUS_NAMES.get(self.status, self.status)