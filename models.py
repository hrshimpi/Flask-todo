from dataclasses import dataclass, field
from datetime import date, datetime

@dataclass
class Todo:
    _id: str
    title: str
    description: str
    created_at: datetime = datetime.now()
    due_date: datetime = None
    # created_at: date = datetime.now()
    # due_date: date = None

@dataclass
class User:
    _id: str
    email: str
    password: str
    todos: list[str] = field(default_factory=list)