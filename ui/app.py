import customtkinter as ctk
from ui.views.main_view import MainView
from utils.theme import Theme

class TodoApp(ctk.CTk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        
        # Configure window
        self.title("Professional Task Manager")
        self.geometry("1000x700")
        self.minsize(800, 600)
        self.configure(fg_color=Theme.BG)
        
        # Create main view
        self.main_view = MainView(self, self.controller)
        self.main_view.pack(fill="both", expand=True, padx=20, pady=20)
