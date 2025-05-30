import customtkinter as ctk
from ui.app import TodoApp
from app.repositories import TaskRepository
from app.controllers import TaskController
from utils.theme import Theme

if __name__ == "__main__":
    # Configure UI
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme(Theme.get_theme_path())
    
    # Initialize application components
    repository = TaskRepository()
    controller = TaskController(repository)
    
    # Create and run app
    app = TodoApp(controller)
    app.mainloop()
