from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Lesson:
    lesson_id: int | None = None
    date: str = ""
    group_id: int | None = None
    teacher_id: int | None = None

    group_name: str | None = None
    teacher_name: str | None = None