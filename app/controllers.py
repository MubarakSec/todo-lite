from app.repositories import TaskRepository
from app.models import Task
from app.services import NotificationService

class TaskController:
    def __init__(self, repository: TaskRepository):
        self.repository = repository
        self.notification_service = NotificationService()
    
    def create_task(self, task_data: dict) -> Task:
        task = Task(**task_data)
        self.repository.save(task)
        self.notification_service.notify("Task created", f"Created '{task.title}'")
        return task
    
    def update_task(self, task_id: str, task_data: dict) -> Task:
        task = self.repository.get_by_id(task_id)
        if not task:
            raise ValueError("Task not found")
        
        for key, value in task_data.items():
            setattr(task, key, value)
        
        self.repository.save(task)
        self.notification_service.notify("Task updated", f"Updated '{task.title}'")
        return task
    
    def delete_task(self, task_id: str) -> None:
        task = self.repository.get_by_id(task_id)
        if task:
            self.repository.delete(task_id)
            self.notification_service.notify("Task deleted", f"Deleted '{task.title}'")
    
    def get_all_tasks(self) -> list:
        return self.repository.get_all()
    
    def get_tasks_by_status(self, completed: bool = None, pinned: bool = None) -> list:
        return self.repository.filter(completed=completed, pinned=pinned)
    
    def search_tasks(self, query: str) -> list:
        return self.repository.search(query)
    
    def toggle_completion(self, task_id: str) -> Task:
        task = self.repository.get_by_id(task_id)
        if task:
            task.completed = not task.completed
            self.repository.save(task)
            status = "completed" if task.completed else "marked incomplete"
            self.notification_service.notify("Task updated", f"{status} '{task.title}'")
            return task
        return None
    
    def toggle_pin(self, task_id: str) -> Task:
        task = self.repository.get_by_id(task_id)
        if task:
            task.pinned = not task.pinned
            self.repository.save(task)
            status = "pinned" if task.pinned else "unpinned"
            self.notification_service.notify("Task updated", f"{status} '{task.title}'")
            return task
        return None
    
    def get_task_statistics(self) -> dict:
        tasks = self.repository.get_all()
        total = len(tasks)
        completed = sum(1 for t in tasks if t.completed)
        active = sum(1 for t in tasks if not t.completed)
        pinned = sum(1 for t in tasks if t.pinned and not t.completed)
        return {
            "total": total,
            "completed": completed,
            "active": active,
            "pinned": pinned
        }
    
    def get_all_tags(self) -> list:
        tags = set()
        for task in self.repository.get_all():
            tags.update(task.tags)
        return sorted(tags)
