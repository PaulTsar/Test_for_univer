from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Student:
    student_id: int | None = None
    full_name: str = ""
    group_id: int | None = None

    group_name: str | None = None