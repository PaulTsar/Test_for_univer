from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Group:
    group_id: int | None = None
    name: str = ""