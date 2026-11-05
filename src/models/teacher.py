from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Teacher:
    teacher_id: int | None = None
    full_name: str = ""