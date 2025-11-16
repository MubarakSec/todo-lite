import customtkinter as ctk
import tkinter as tk
from datetime import datetime
from app.models import Task
from ui.components.date_picker import DatePicker
from utils.theme import Theme

class TaskDialog(ctk.CTkToplevel):
    def __init__(self, parent, task=None, all_tags=None):
        super().__init__(parent)
        self.parent = parent
        self.task = task
        self.all_tags = all_tags or []
        self.title("Create Task" if not task else "Edit Task")
        self.geometry("600x550")
        self.resizable(False, False)
        self.configure(fg_color=Theme.BG)
        
        # Bring dialog to front
        self.lift()
        self.attributes('-topmost', True)
        self.after(100, lambda: self.attributes('-topmost', False))
        self.focus_set()
        
        # Professional header
        header_frame = ctk.CTkFrame(self, fg_color=Theme.HEADER, height=50, corner_radius=0)
        header_frame.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(
            header_frame,
            text="TASK DETAILS",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=Theme.TEXT
        ).pack(side="left", padx=20)
        
        # Main content
        content_frame = ctk.CTkFrame(self, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Form grid
        content_frame.grid_columnconfigure(1, weight=1)
        row = 0
        
        # Title field
        ctk.CTkLabel(
            content_frame,
            text="Title *",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=Theme.TEXT,
            anchor="w"
        ).grid(row=row, column=0, padx=(0, 10), pady=(0, 5), sticky="w")
        
        self.title_entry = ctk.CTkEntry(
            content_frame,
            placeholder_text="Enter task title...",
            fg_color=Theme.CARD,
            border_color=Theme.BORDER,
            corner_radius=Theme.CORNER_RADIUS,
            height=40
        )
        self.title_entry.grid(row=row, column=1, sticky="ew", pady=(0, 15))
        row += 1
        
        # Description field
        ctk.CTkLabel(
            content_frame,
            text="Description",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=Theme.TEXT,
            anchor="w"
        ).grid(row=row, column=0, padx=(0, 10), pady=(0, 5), sticky="w")
        
        self.desc_entry = ctk.CTkTextbox(
            content_frame,
            height=100,
            fg_color=Theme.CARD,
            border_color=Theme.BORDER,
            corner_radius=Theme.CORNER_RADIUS
        )
        self.desc_entry.grid(row=row, column=1, sticky="ew", pady=(0, 15))
        row += 1
        
        # Due date field
        ctk.CTkLabel(
            content_frame,
            text="Due Date",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=Theme.TEXT,
            anchor="w"
        ).grid(row=row, column=0, padx=(0, 10), pady=(0, 5), sticky="w")
        
        date_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        date_frame.grid(row=row, column=1, sticky="ew", pady=(0, 15))
        
        self.date_var = tk.StringVar()
        self.date_entry = ctk.CTkEntry(
            date_frame,
            textvariable=self.date_var,
            placeholder_text="YYYY-MM-DD",
            fg_color=Theme.CARD,
            border_color=Theme.BORDER,
            corner_radius=Theme.CORNER_RADIUS,
            height=40
        )
        self.date_entry.pack(side="left", fill="x", expand=True)
        
        self.cal_btn = ctk.CTkButton(
            date_frame,
            text="📅",
            width=40,
            height=40,
            command=self.open_calendar
        )
        self.cal_btn.pack(side="left", padx=(10, 0))
        
        self.clear_date_btn = ctk.CTkButton(
            date_frame,
            text="Clear",
            width=60,
            height=40,
            fg_color="transparent",
            border_width=1,
            border_color=Theme.BORDER,
            text_color=Theme.TEXT,
            command=self.clear_due_date
        )
        self.clear_date_btn.pack(side="left", padx=(10, 0))
        row += 1
        
        # Priority field
        ctk.CTkLabel(
            content_frame,
            text="Priority",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=Theme.TEXT,
            anchor="w"
        ).grid(row=row, column=0, padx=(0, 10), pady=(0, 5), sticky="w")
        
        self.priority_var = tk.StringVar(value="Medium")
        priority_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        priority_frame.grid(row=row, column=1, sticky="w", pady=(0, 15))
        
        priorities = [("High", "High"), ("Medium", "Medium"), ("Low", "Low")]
        for text, value in priorities:
            btn = ctk.CTkRadioButton(
                priority_frame,
                text=text,
                variable=self.priority_var,
                value=value,
                text_color=Theme.TEXT
            )
            btn.pack(side="left", padx=(0, 20))
        row += 1
        
        # Tags field
        ctk.CTkLabel(
            content_frame,
            text="Tags",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=Theme.TEXT,
            anchor="w"
        ).grid(row=row, column=0, padx=(0, 10), pady=(0, 5), sticky="w")
        
        self.tags_entry = ctk.CTkEntry(
            content_frame,
            placeholder_text="work, personal, urgent...",
            fg_color=Theme.CARD,
            border_color=Theme.BORDER,
            corner_radius=Theme.CORNER_RADIUS,
            height=40
        )
        self.tags_entry.grid(row=row, column=1, sticky="ew", pady=(0, 10))
        row += 1
        
        ctk.CTkLabel(
            content_frame,
            text="Separate tags with commas or tap a recent tag below.",
            font=ctk.CTkFont(size=11),
            text_color=Theme.TEXT_SECONDARY,
            anchor="w"
        ).grid(row=row, column=1, sticky="w", pady=(0, 12))
        row += 1
        
        # Recent tags - FIXED: Using solid color instead of alpha
        if self.all_tags:
            ctk.CTkLabel(
                content_frame,
                text="Recent Tags:",
                font=ctk.CTkFont(size=11),
                text_color=Theme.TEXT_SECONDARY,
                anchor="w"
            ).grid(row=row, column=1, sticky="w", pady=(0, 5))
            row += 1
            
            tags_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
            tags_frame.grid(row=row, column=1, sticky="w", pady=(0, 15))
            
            for tag in self.all_tags[:5]:
                btn = ctk.CTkButton(
                    tags_frame,
                    text=tag,
                    corner_radius=12,
                    height=28,
                    fg_color=Theme.TAG_BG,  # Fixed: Using solid color
                    hover_color=Theme.ACCENT_HOVER,
                    text_color=Theme.ACCENT,
                    font=ctk.CTkFont(size=11),
                    command=lambda t=tag: self.add_tag(t)
                )
                btn.pack(side="left", padx=(0, 8))
            row += 1
        
        # Action buttons
        button_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        button_frame.grid(row=row, column=1, sticky="e", pady=(20, 0))
        
        self.cancel_btn = ctk.CTkButton(
            button_frame,
            text="Cancel",
            width=100,
            height=40,
            fg_color="transparent",
            border_width=1,
            border_color=Theme.BORDER,
            text_color=Theme.TEXT,
            command=self.destroy
        )
        self.cancel_btn.pack(side="right", padx=(10, 0))
        
        self.save_btn = ctk.CTkButton(
            button_frame,
            text="Save Task",
            width=120,
            height=40,
            fg_color=Theme.ACCENT,
            hover_color=Theme.ACCENT_HOVER,
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self.save_task
        )
        self.save_btn.pack(side="right")
        
        # Populate if editing
        if task:
            self.title_entry.insert(0, task.title)
            if task.description:
                self.desc_entry.insert("1.0", task.description)
            if task.due_date:
                self.date_var.set(task.due_date)
            self.priority_var.set(task.priority)
            if task.tags:
                self.tags_entry.insert(0, ", ".join(task.tags))
        
        # Focus title field
        self.title_entry.focus_set()
        
        self.grab_set()
        self.transient(self.parent)
        self.wait_window()
    
    def open_calendar(self):
        initial_date = self.date_var.get() or datetime.now().strftime("%Y-%m-%d")
        calendar = DatePicker(self, initial_date)
        if calendar.selected_date:
            self.date_var.set(calendar.selected_date)
    
    def save_task(self):
        title = self.title_entry.get().strip()
        if not title:
            tk.messagebox.showerror("Validation Error", "Title is required")
            return
        
        description = self.desc_entry.get("1.0", "end-1c").strip()
        due_date = self.date_var.get().strip()
        priority = self.priority_var.get()
        tags = [tag.strip() for tag in self.tags_entry.get().split(",") if tag.strip()]
        
        if due_date:
            try:
                datetime.strptime(due_date, "%Y-%m-%d")
            except ValueError:
                tk.messagebox.showerror("Validation Error", "Due date must follow YYYY-MM-DD.")
                return
        
        if self.task:
            # Update existing task
            self.task.title = title
            self.task.description = description
            self.task.due_date = due_date if due_date else None
            self.task.priority = priority
            self.task.tags = tags
        else:
            # Create new task
            self.task = Task(
                title=title,
                description=description,
                due_date=due_date if due_date else None,
                priority=priority,
                tags=tags
            )
        
        self.destroy()
    
    def add_tag(self, tag):
        current_tags = self.tags_entry.get().strip()
        if current_tags:
            # Check if tag already exists
            tags_list = [t.strip() for t in current_tags.split(",")]
            if tag not in tags_list:
                self.tags_entry.insert("end", f", {tag}")
        else:
            self.tags_entry.insert("end", tag)

    def clear_due_date(self):
        self.date_var.set("")
