import json
import os
from app.models import Task

class TaskRepository:
    def __init__(self, filename="data.json"):
        self.filename = filename
        self.tasks = self._load_tasks()
    
    def _load_tasks(self) -> list:
        if not os.path.exists(self.filename):
            return []
        
        try:
            with open(self.filename, "r") as f:
                data = json.load(f)
                return [Task.from_dict(item) for item in data]
        except (json.JSONDecodeError, IOError):
            return []
    
    def _save_tasks(self):
        data = [task.to_dict() for task in self.tasks]
        try:
            with open(self.filename, "w") as f:
                json.dump(data, f, indent=2)
        except IOError:
            pass
    
    def save(self, task: Task):
        # Update existing or add new
        existing_index = next((i for i, t in enumerate(self.tasks) if t.id == task.id), None)
        if existing_index is not None:
            self.tasks[existing_index] = task
        else:
            self.tasks.append(task)
        self._save_tasks()
    
    def get_by_id(self, task_id: str):
        return next((t for t in self.tasks if t.id == task_id), None)
    
    def get_all(self) -> list:
        return self.tasks.copy()
    
    def delete(self, task_id: str):
        self.tasks = [t for t in self.tasks if t.id != task_id]
        self._save_tasks()
    
    def filter(self, completed: bool = None, 
              pinned: bool = None) -> list:
        result = []
        for task in self.tasks:
            if completed is not None and task.completed != completed:
                continue
            if pinned is not None and task.pinned != pinned:
                continue
            result.append(task)
        return result
    
    def search(self, query: str) -> list:
        if not query:
            return self.tasks.copy()
        
        query = query.lower()
        results = []
        for task in self.tasks:
            if (query in task.title.lower() or 
                (task.description and query in task.description.lower()) or
                (task.due_date and query in task.due_date) or
                any(query in tag.lower() for tag in task.tags)):
                results.append(task)
        return results
