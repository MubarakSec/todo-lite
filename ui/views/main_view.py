import customtkinter as ctk
import tkinter as tk
import random
from datetime import datetime
from ui.components.task_card import TaskCard
from ui.components.task_dialog import TaskDialog
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
            width=44,
            height=44,
            corner_radius=22,
            command=self.toggle_theme,
            fg_color=Theme.CARD,
            hover_color=Theme.HOVER,
            text_color=Theme.TEXT,
            border_width=1,
            border_color=Theme.BORDER
        )
        self.theme_btn.grid(row=0, column=10, padx=(10, 20), sticky="e")
        self._update_theme_button()
        
        # Main content area
        self.content_frame = ctk.CTkFrame(self, fg_color=Theme.BG)
        self.content_frame.grid(row=1, column=0, sticky="nsew", pady=(20, 0))
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(1, weight=1)
        
        # Tab control - segmented button inside elevated container
        self.tab_container = ctk.CTkFrame(
            self.content_frame,
            fg_color=Theme.CARD,
            corner_radius=Theme.CORNER_RADIUS,
            border_width=1,
            border_color=Theme.BORDER
        )
        self.tab_container.grid(row=0, column=0, sticky="ew")
        self.tab_container.grid_columnconfigure(0, weight=1)
        
        self.tab_buttons = ctk.CTkSegmentedButton(
            self.tab_container,
            values=["All Tasks", "Active", "Completed", "Pinned"],
            fg_color=Theme.CARD,
            selected_color=Theme.ACCENT,
            selected_hover_color=Theme.ACCENT_HOVER,
            unselected_color=Theme.BG,
            unselected_hover_color=Theme.HOVER,
            text_color=Theme.TEXT,
            command=self.on_tab_change
        )
        self.tab_buttons.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.tab_buttons.set("All Tasks")
        
        # Search / filter card
        self.action_card = ctk.CTkFrame(
            self.content_frame,
            fg_color=Theme.CARD,
            corner_radius=Theme.CORNER_RADIUS,
            border_width=1,
            border_color=Theme.BORDER
        )
        self.action_card.grid(row=1, column=0, sticky="ew", pady=(12, 0))
        self.action_card.grid_columnconfigure(0, weight=1)
        self.action_card.grid_columnconfigure(1, weight=0)
        self.action_card.grid_columnconfigure(2, weight=0)
        
        # Search input - store as instance variable
        self.search_entry = ctk.CTkEntry(
            self.action_card,
            placeholder_text="Search tasks...",
            fg_color=Theme.CARD,
            border_color=Theme.BORDER,
            corner_radius=Theme.CORNER_RADIUS,
            height=40
        )
        self.search_entry.bind("<KeyRelease>", self.on_search_change)
        
        # Sorting dropdown for better control
        self.sort_var = tk.StringVar(value="Recently Added")
        self.sort_menu = ctk.CTkOptionMenu(
            self.action_card,
            values=["Recently Added", "Due Date", "Priority"],
            variable=self.sort_var,
            command=lambda choice: self.refresh_tasks(),
            fg_color=Theme.CARD,
            button_color=Theme.ACCENT,
            button_hover_color=Theme.ACCENT_HOVER,
            dropdown_fg_color=Theme.CARD,
            dropdown_hover_color=Theme.HOVER,
            dropdown_text_color=Theme.TEXT,
            text_color=Theme.TEXT
        )
        self.search_entry.grid(row=0, column=0, sticky="ew", padx=16, pady=16)
        self.sort_menu.grid(row=0, column=1, padx=(0, 16), pady=16)
        
        # Add button - store as instance variable
        self.add_btn = ctk.CTkButton(
            self.action_card,
            text="+ Add Task",
            width=120,
            height=40,
            corner_radius=Theme.CORNER_RADIUS,
            fg_color=Theme.ACCENT,
            hover_color=Theme.ACCENT_HOVER,
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self.add_task
        )
        self.add_btn.grid(row=0, column=2, padx=(0, 16), pady=16)
        
        # Overdue filter toggle
        self.overdue_filter_var = tk.BooleanVar(value=False)
        self.overdue_switch = ctk.CTkSwitch(
            self.action_card,
            text="Show overdue only",
            variable=self.overdue_filter_var,
            command=self.refresh_tasks,
            fg_color=Theme.CARD,
            button_color=Theme.ACCENT,
            button_hover_color=Theme.ACCENT_HOVER,
            text_color=Theme.TEXT
        )
        self.overdue_switch.grid(row=1, column=0, columnspan=3, sticky="w", padx=16, pady=(0, 16))
        
        # Task list area
        self.task_frame = ctk.CTkFrame(self.content_frame, fg_color=Theme.BG)
        self.task_frame.grid(row=2, column=0, sticky="nsew", pady=(15, 0))
        self.task_frame.grid_columnconfigure(0, weight=1)
        self.task_frame.grid_rowconfigure(0, weight=1)
        
        # Create scrollable container for tasks
        self.scroll_frame = ctk.CTkScrollableFrame(
            self.task_frame, 
            fg_color=Theme.BG
        )
        self.scroll_frame.grid(row=0, column=0, sticky="nsew")
        self.scroll_frame.grid_columnconfigure(0, weight=1)
        
        # Task statistics footer
        self.stats_frame = ctk.CTkFrame(
            self,
            fg_color=Theme.CARD,
            height=48,
            corner_radius=Theme.CORNER_RADIUS,
            border_width=1,
            border_color=Theme.BORDER
        )
        self.stats_frame.grid(row=2, column=0, sticky="ew", pady=(20, 0))
        
        stats = self.controller.get_task_statistics()
        self.stats_label = ctk.CTkLabel(
            self.stats_frame,
            text=f"Tasks: {stats['total']} | Active: {stats['active']} | Completed: {stats['completed']} | Pinned: {stats['pinned']}",
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
        self._update_theme_button()
        
        # Update all UI elements
        self.configure(fg_color=Theme.BG)
        
        # Header
        self.header_frame.configure(fg_color=Theme.HEADER)
        self.title_label.configure(text_color=Theme.TEXT)
        self.quote_label.configure(text_color=Theme.TEXT_SECONDARY)
        self.content_frame.configure(fg_color=Theme.BG)
        
        # Tab control
        self.tab_container.configure(
            fg_color=Theme.CARD,
            border_color=Theme.BORDER
        )
        self.tab_buttons.configure(
            fg_color=Theme.CARD,
            selected_color=Theme.ACCENT,
            selected_hover_color=Theme.ACCENT_HOVER,
            unselected_color=Theme.BG,
            unselected_hover_color=Theme.HOVER,
            text_color=Theme.TEXT
        )
        
        # Search and add card
        self.action_card.configure(
            fg_color=Theme.CARD,
            border_color=Theme.BORDER
        )
        self.search_entry.configure(
            fg_color=Theme.CARD,
            border_color=Theme.BORDER
        )
        self.sort_menu.configure(
            fg_color=Theme.CARD,
            button_color=Theme.ACCENT,
            button_hover_color=Theme.ACCENT_HOVER,
            dropdown_fg_color=Theme.CARD,
            dropdown_hover_color=Theme.HOVER,
            dropdown_text_color=Theme.TEXT,
            text_color=Theme.TEXT
        )
        self.add_btn.configure(
            fg_color=Theme.ACCENT,
            hover_color=Theme.ACCENT_HOVER
        )
        self.overdue_switch.configure(
            fg_color=Theme.CARD,
            button_color=Theme.ACCENT,
            button_hover_color=Theme.ACCENT_HOVER,
            text_color=Theme.TEXT
        )
        
        # Task area
        self.task_frame.configure(fg_color=Theme.BG)
        self.scroll_frame.configure(fg_color=Theme.BG)
        
        # Stats footer
        self.stats_frame.configure(
            fg_color=Theme.CARD,
            border_color=Theme.BORDER
        )
        self.stats_label.configure(text_color=Theme.TEXT_SECONDARY)
        
        # Context menu
        self.context_menu.configure(bg=Theme.MENU, fg=Theme.TEXT)
        
        self.refresh_tasks()
    
    def _update_theme_button(self):
        icon = "☾" if Theme.MODE == "dark" else "☀"
        self.theme_btn.configure(
            text=icon,
            fg_color=Theme.CARD,
            hover_color=Theme.HOVER,
            text_color=Theme.TEXT,
            border_color=Theme.BORDER
        )
    
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
        
        tasks = self._get_tasks_for_current_tab()
        search_query = self.search_entry.get().strip().lower()
        
        if search_query:
            tasks = [task for task in tasks if self._matches_search(task, search_query)]
        
        if self.overdue_filter_var.get():
            tasks = [task for task in tasks if self._is_overdue(task)]
        
        tasks = self._sort_tasks(tasks)
        
        if tasks:
            for i, task in enumerate(tasks):
                card = TaskCard(
                    self.scroll_frame,
                    task,
                    self.on_task_action
                )
                card.grid(row=i, column=0, pady=(0, 12), sticky="ew")
        else:
            self._render_empty_state(bool(search_query or self.overdue_filter_var.get()))
        
        stats = self.controller.get_task_statistics()
        self.stats_label.configure(
            text=f"Tasks: {stats['total']} | Active: {stats['active']} | Completed: {stats['completed']} | Pinned: {stats['pinned']}"
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

    def _get_tasks_for_current_tab(self):
        if self.current_tab == "all":
            return self.controller.get_all_tasks()
        if self.current_tab == "pinned":
            # Completed pinned tasks add noise; hide them here
            return self.controller.get_tasks_by_status(completed=False, pinned=True)
        if self.current_tab == "active":
            return self.controller.get_tasks_by_status(completed=False)
        if self.current_tab == "completed":
            return self.controller.get_tasks_by_status(completed=True)
        return self.controller.get_all_tasks()
    
    def _matches_search(self, task, query):
        if not query:
            return True
        in_title = query in task.title.lower()
        in_desc = bool(task.description and query in task.description.lower())
        in_due = bool(task.due_date and query in task.due_date.lower())
        in_tags = any(query in tag.lower() for tag in task.tags)
        return in_title or in_desc or in_due or in_tags
    
    def _is_overdue(self, task):
        due_date = self._parse_due_date(task.due_date)
        if not due_date:
            return False
        today = datetime.now().date()
        return due_date < today and not task.completed
    
    def _sort_tasks(self, tasks):
        sort_option = self.sort_var.get()
        priority_weights = {"High": 0, "Medium": 1, "Low": 2}
        
        def created_at_key(task):
            try:
                return datetime.fromisoformat(task.created_at).timestamp()
            except (TypeError, ValueError):
                return 0
        
        def due_date_key(task):
            due = self._parse_due_date(task.due_date)
            return due or datetime.max.date()
        
        if sort_option == "Due Date":
            tasks.sort(key=lambda t: (0 if t.pinned else 1, due_date_key(t)))
        elif sort_option == "Priority":
            tasks.sort(key=lambda t: (0 if t.pinned else 1, priority_weights.get(t.priority, 3), due_date_key(t)))
        else:  # Recently Added
            tasks.sort(key=lambda t: (0 if t.pinned else 1, -created_at_key(t)))
        return tasks
    
    def _parse_due_date(self, due_date_str):
        if not due_date_str:
            return None
        try:
            return datetime.strptime(due_date_str, "%Y-%m-%d").date()
        except ValueError:
            return None
    
    def _render_empty_state(self, filtered):
        empty_frame = ctk.CTkFrame(
            self.scroll_frame,
            fg_color=Theme.CARD,
            corner_radius=Theme.CORNER_RADIUS,
            border_width=1,
            border_color=Theme.BORDER
        )
        empty_frame.grid(row=0, column=0, sticky="nsew", pady=40, padx=10)
        empty_frame.grid_columnconfigure(0, weight=1)
        
        title = "No matching tasks" if filtered else "You're all caught up!"
        subtitle = (
            "Try adjusting your filters or search terms."
            if filtered else
            "Add a task to get started and keep everything on track."
        )
        
        ctk.CTkLabel(
            empty_frame,
            text=title,
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color=Theme.TEXT
        ).grid(row=0, column=0, pady=(20, 6), padx=20)
        
        ctk.CTkLabel(
            empty_frame,
            text=subtitle,
            font=ctk.CTkFont(size=13),
            text_color=Theme.TEXT_SECONDARY,
            wraplength=400
        ).grid(row=1, column=0, padx=20)
        
        if not filtered:
            ctk.CTkButton(
                empty_frame,
                text="Add a task",
                fg_color=Theme.ACCENT,
                hover_color=Theme.ACCENT_HOVER,
                command=self.add_task
            ).grid(row=2, column=0, pady=(20, 20))
