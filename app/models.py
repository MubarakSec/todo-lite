import uuid
from datetime import datetime

class Task:
    def __init__(self, 
                 title: str, 
                 description: str = None,
                 due_date: str = None,
                 priority: str = "Medium",
                 tags: list = None,
                 created_at: str = None,
                 completed: bool = False,
                 pinned: bool = False):
        self.id = str(uuid.uuid4())
        self.title = title
        self.description = description
        self.due_date = due_date
        self.priority = priority
        self.tags = tags or []
        self.created_at = created_at or datetime.now().isoformat()
        self.completed = completed
        self.pinned = pinned
    
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date,
            "priority": self.priority,
            "tags": self.tags,
            "created_at": self.created_at,
            "completed": self.completed,
            "pinned": self.pinned
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            title=data["title"],
            description=data.get("description"),
            due_date=data.get("due_date"),
            priority=data.get("priority", "Medium"),
            tags=data.get("tags", []),
            created_at=data.get("created_at"),
            completed=data.get("completed", False),
            pinned=data.get("pinned", False)
        )
