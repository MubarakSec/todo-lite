import customtkinter as ctk
import tkinter as tk
import random
from ui.components.task_card import TaskCard
from ui.components.task_dialog import TaskDialog
from ui.components.date_picker import DatePicker
from utils.theme import Theme

class MainView(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=Theme.BG)
        self.controller = controller
        self.parent = parent
        self.current_tab = "all"
        
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Professional header - store as instance variable
        self.header_frame = ctk.CTkFrame(self, fg_color=Theme.HEADER, height=60, corner_radius=0)
        self.header_frame.grid(row=0, column=0, sticky="ew")
        self.header_frame.grid_columnconfigure(0, weight=1)
        
        # App title
        self.title_label = ctk.CTkLabel(
            self.header_frame,
            text="TASK MANAGER",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=Theme.TEXT
        )
        self.title_label.grid(row=0, column=0, padx=20, sticky="w")
        
        # Professional quote display
        self.quotes = [
            "Productivity is being able to do things that you were never able to do before.",
            "The secret of getting ahead is getting started.",
            "Do the hard jobs first. The easy jobs will take care of themselves.",
            "Your future is created by what you do today, not tomorrow.",
            "Small daily improvements are the key to staggering long-term results."
        ]
        
        self.quote_label = ctk.CTkLabel(
            self.header_frame,
            text=random.choice(self.quotes),
            font=ctk.CTkFont(size=12, slant="italic"),
            text_color=Theme.TEXT_SECONDARY,
            wraplength=400
        )
        self.quote_label.grid(row=0, column=1, padx=20, sticky="ew")
        
        # Theme toggle button
        self.theme_btn = ctk.CTkButton(
            self.header_frame,
            text="🌙" if Theme.BG == Theme.DARK_BG else "🌞",
            width=40,
            height=40,
            corner_radius=20,
            fg_color=Theme.CARD,
            hover_color=Theme.HOVER,
            command=self.toggle_theme
        )
        self.theme_btn.grid(row=0, column=10, padx=(10, 20), sticky="e")
        
        # Main content area
        content_frame = ctk.CTkFrame(self, fg_color="transparent")
        content_frame.grid(row=1, column=0, sticky="nsew", pady=(20, 0))
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_rowconfigure(1, weight=1)
        
        # Tab control - store as instance variable
        self.tab_frame = ctk.CTkFrame(content_frame, fg_color="transparent", height=40)
        self.tab_frame.grid(row=0, column=0, sticky="ew")
        self.tab_frame.grid_columnconfigure(0, weight=1)
        
        self.tabview = ctk.CTkTabview(
            self.tab_frame, 
            height=40,
            fg_color="transparent",
            segmented_button_selected_color=Theme.ACCENT,
            segmented_button_selected_hover_color=Theme.ACCENT_HOVER,
            segmented_button_unselected_color=Theme.BG,
            segmented_button_unselected_hover_color=Theme.HOVER
        )
        self.tabview.grid(row=0, column=0, sticky="ew")
        
        self.tabs = {
            "all": self.tabview.add("All Tasks"),
            "active": self.tabview.add("Active"),
            "completed": self.tabview.add("Completed"),
            "pinned": self.tabview.add("Pinned")
        }
        
        # Set tab selection callback
        self.tabview.configure(command=self._tabview_callback)
        self.tabview.set("All Tasks")
        
        # Search and add task bar
        self.action_frame = ctk.CTkFrame(content_frame, fg_color="transparent", height=50)
        self.action_frame.grid(row=1, column=0, sticky="ew", pady=(10, 0))
        self.action_frame.grid_columnconfigure(0, weight=1)
        
        # Search input - store as instance variable
        self.search_entry = ctk.CTkEntry(
            self.action_frame,
            placeholder_text="Search tasks...",
            fg_color=Theme.CARD,
            border_color=Theme.BORDER,
            corner_radius=Theme.CORNER_RADIUS,
            height=40
        )
        self.search_entry.grid(row=0, column=0, sticky="ew")
        self.search_entry.bind("<KeyRelease>", self.on_search_change)
        
        # Add button - store as instance variable
        self.add_btn = ctk.CTkButton(
            self.action_frame,
            text="+ Add Task",
            width=120,
            height=40,
            corner_radius=Theme.CORNER_RADIUS,
            fg_color=Theme.ACCENT,
            hover_color=Theme.ACCENT_HOVER,
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self.add_task
        )
        self.add_btn.grid(row=0, column=1, padx=(10, 0))
        
        # Task list area
        self.task_frame = ctk.CTkFrame(content_frame)
        self.task_frame.grid(row=2, column=0, sticky="nsew", pady=(15, 0))
        self.task_frame.grid_columnconfigure(0, weight=1)
        self.task_frame.grid_rowconfigure(0, weight=1)
        
        # Create scrollable container for tasks
        self.scroll_frame = ctk.CTkScrollableFrame(
            self.task_frame, 
            fg_color="transparent"
        )
        self.scroll_frame.grid(row=0, column=0, sticky="nsew")
        self.scroll_frame.grid_columnconfigure(0, weight=1)
        
        # Task statistics footer
        self.stats_frame = ctk.CTkFrame(self, fg_color=Theme.HEADER, height=40, corner_radius=6)
        self.stats_frame.grid(row=2, column=0, sticky="ew", pady=(20, 0))
        
        stats = self.controller.get_task_statistics()
        self.stats_label = ctk.CTkLabel(
            self.stats_frame,
            text=f"Tasks: {stats['total']} • Active: {stats['active']} • Completed: {stats['completed']} • Pinned: {stats['pinned']}",
            font=ctk.CTkFont(size=12),
            text_color=Theme.TEXT_SECONDARY
        )
        self.stats_label.pack(side="left", padx=20)
        
        # Bind keyboard shortcuts
        self.parent.bind("<Control-n>", lambda e: self.add_task())
        self.parent.bind("<Control-f>", lambda e: self.search_entry.focus())
        
        # Right-click context menu
        self.context_menu = tk.Menu(self, tearoff=0, bg=Theme.MENU, fg=Theme.TEXT)
        self.context_menu.add_command(label="New Task", command=self.add_task)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Refresh", command=self.refresh_tasks)
        self.bind("<Button-3>", self.show_context_menu)
        
        # Load tasks
        self.refresh_tasks()
        
        # Change quote every 30 seconds
        self.after(30000, self.change_quote)
    
    def toggle_theme(self):
        Theme.toggle_theme()
        self.theme_btn.configure(text="🌞" if Theme.BG == Theme.DARK_BG else "🌙")
        
        # Update all UI elements
        self.configure(fg_color=Theme.BG)
        
        # Header
        self.header_frame.configure(fg_color=Theme.HEADER)
        self.title_label.configure(text_color=Theme.TEXT)
        self.quote_label.configure(text_color=Theme.TEXT_SECONDARY)
        self.theme_btn.configure(hover_color=Theme.HOVER)
        
        # Tab control
        self.tab_frame.configure(fg_color="transparent")
        self.tabview.configure(
            segmented_button_selected_color=Theme.ACCENT,
            segmented_button_selected_hover_color=Theme.ACCENT_HOVER,
            segmented_button_unselected_color=Theme.BG,
            segmented_button_unselected_hover_color=Theme.HOVER
        )
        
        # Search and add
        self.action_frame.configure(fg_color="transparent")
        self.search_entry.configure(
            fg_color=Theme.CARD,
            border_color=Theme.BORDER
        )
        self.add_btn.configure(
            fg_color=Theme.ACCENT,
            hover_color=Theme.ACCENT_HOVER
        )
        
        # Task area
        self.task_frame.configure(fg_color="transparent")
        
        # Stats footer
        self.stats_frame.configure(fg_color=Theme.HEADER)
        self.stats_label.configure(text_color=Theme.TEXT_SECONDARY)
        
        # Context menu
        self.context_menu.configure(bg=Theme.MENU, fg=Theme.TEXT)
        
        self.refresh_tasks()
    
    def _tabview_callback(self):
        selected_tab = self.tabview.get()
        self.on_tab_change(selected_tab)
    
    def on_tab_change(self, selected_tab):
        self.current_tab = self.get_tab_key(selected_tab)
        self.refresh_tasks()
    
    def get_tab_key(self, tab_name):
        mapping = {
            "All Tasks": "all",
            "Active": "active",
            "Completed": "completed",
            "Pinned": "pinned"
        }
        return mapping.get(tab_name, "all")
    
    def change_quote(self):
        new_quote = random.choice(self.quotes)
        self.quote_label.configure(text=new_quote)
        self.after(30000, self.change_quote)
    
    def show_context_menu(self, event):
        try:
            self.context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()
    
    def refresh_tasks(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
        
        search_query = self.search_entry.get().strip()
        
        if search_query:
            tasks = self.controller.search_tasks(search_query)
        else:
            if self.current_tab == "all":
                tasks = self.controller.get_all_tasks()
            elif self.current_tab == "pinned":
                tasks = self.controller.get_tasks_by_status(pinned=True)
            elif self.current_tab == "active":
                tasks = self.controller.get_tasks_by_status(completed=False)
            elif self.current_tab == "completed":
                tasks = self.controller.get_tasks_by_status(completed=True)
        
        if tasks:
            for i, task in enumerate(tasks):
                card = TaskCard(
                    self.scroll_frame,
                    task,
                    self.on_task_action
                )
                card.grid(row=i, column=0, pady=(0, 12), sticky="ew")
        else:
            no_tasks_label = ctk.CTkLabel(
                self.scroll_frame,
                text="No tasks found" if search_query else f"No {self.current_tab} tasks",
                font=ctk.CTkFont(size=14),
                text_color=Theme.TEXT_SECONDARY,
                height=100
            )
            no_tasks_label.grid(row=0, column=0, sticky="nsew")
        
        stats = self.controller.get_task_statistics()
        self.stats_label.configure(
            text=f"Tasks: {stats['total']} • Active: {stats['active']} • Completed: {stats['completed']} • Pinned: {stats['pinned']}"
        )
    
    def on_search_change(self, event=None):
        self.refresh_tasks()
    
    def on_task_action(self, action, task):
        if action == "complete":
            self.controller.toggle_completion(task.id)
        elif action == "edit":
            self.edit_task(task)
        elif action == "delete":
            self.delete_task(task)
        elif action == "pin":
            self.controller.toggle_pin(task.id)
        
        self.refresh_tasks()
    
    def add_task(self, event=None):
        dialog = TaskDialog(self, None, self.controller.get_all_tags())
        if dialog.task:
            self.controller.create_task({
                "title": dialog.task.title,
                "description": dialog.task.description,
                "due_date": dialog.task.due_date,
                "priority": dialog.task.priority,
                "tags": dialog.task.tags,
                "completed": False,
                "pinned": False
            })
            self.refresh_tasks()
    
    def edit_task(self, task):
        dialog = TaskDialog(self, task, self.controller.get_all_tags())
        if dialog.task:
            self.controller.update_task(task.id, {
                "title": dialog.task.title,
                "description": dialog.task.description,
                "due_date": dialog.task.due_date,
                "priority": dialog.task.priority,
                "tags": dialog.task.tags
            })
            self.refresh_tasks()
    
    def delete_task(self, task):
        if tk.messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{task.title}'?"):
            self.controller.delete_task(task.id)
            self.refresh_tasks()
