from __future__ import annotations
from dataclasses import dataclass

ROLE_NAMES = {
    "admin": "Администратор",
    "teacher": "Преподаватель",
    "student": "Студент",
}


@dataclass
class User:
    user_id: int | None = None
    login: str = ""
    password_hash: str = ""
    role: str = "student"
    student_id: int | None = None
    teacher_id: int | None = None

    role_name: str | None = None

    def __post_init__(self):
        if self.role_name is None:
            self.role_name = ROLE_NAMES.get(self.role, self.role)

    @property
    def is_admin(self) -> bool:
        return self.role == "admin"

    @property
    def is_teacher(self) -> bool:
        return self.role == "teacher"

    @property
    def is_student(self) -> bool:
        return self.role == "student"