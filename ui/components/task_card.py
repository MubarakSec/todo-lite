import customtkinter as ctk
import tkinter as tk
from utils.theme import Theme

class TaskCard(ctk.CTkFrame):
    def __init__(self, parent, task, on_action):
        super().__init__(parent, 
                         fg_color=Theme.CARD, 
                         corner_radius=Theme.CORNER_RADIUS,
                         border_width=1,
                         border_color=Theme.BORDER)
        self.task = task
        self.on_action = on_action
        
        # Configure grid
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Checkbox with professional styling
        self.check_var = tk.BooleanVar(value=task.completed)
        self.checkbox = ctk.CTkCheckBox(
            self,
            text="",
            variable=self.check_var,
            command=self.toggle_complete,
            fg_color=Theme.ACCENT,
            hover_color=Theme.ACCENT_HOVER,
            border_width=2,
            border_color=Theme.BORDER,
            width=24,
            height=24
        )
        self.checkbox.grid(row=0, column=0, padx=16, pady=16, sticky="nw")
        
        # Main content area
        content_frame = ctk.CTkFrame(self, fg_color="transparent")
        content_frame.grid(row=0, column=1, padx=(0, 16), pady=16, sticky="nsew")
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_rowconfigure(1, weight=1)
        
        # Task title with professional typography
        self.title_label = ctk.CTkLabel(
            content_frame,
            text=task.title,
            anchor="w",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color=Theme.TEXT
        )
        self.title_label.grid(row=0, column=0, sticky="ew")
        
        # Task description with subtle styling
        self.desc_label = ctk.CTkLabel(
            content_frame,
            text=task.description if task.description else "No description",
            anchor="w",
            font=ctk.CTkFont(size=13),
            text_color=Theme.TEXT_SECONDARY,
            wraplength=400
        )
        self.desc_label.grid(row=1, column=0, sticky="ew", pady=(8, 0))
        
        # Metadata area (priority, due date, tags)
        meta_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        meta_frame.grid(row=2, column=0, sticky="ew", pady=(12, 0))
        
        # Priority indicator with professional styling
        priority_colors = {"High": "#f44336", "Medium": "#ff9800", "Low": "#4caf50"}
        priority_frame = ctk.CTkFrame(meta_frame, fg_color="transparent")
        priority_frame.pack(side="left", padx=(0, 12))
        
        ctk.CTkLabel(
            priority_frame,
            text="●",
            text_color=priority_colors.get(task.priority, "#ff9800"),
            font=ctk.CTkFont(size=10)
        ).pack(side="left")
        
        ctk.CTkLabel(
            priority_frame,
            text=task.priority,
            font=ctk.CTkFont(size=12),
            text_color=Theme.TEXT_SECONDARY
        ).pack(side="left", padx=4)
        
        # Due date with professional styling
        if task.due_date:
            due_frame = ctk.CTkFrame(meta_frame, fg_color="transparent")
            due_frame.pack(side="left", padx=(0, 12))
            
            ctk.CTkLabel(
                due_frame,
                text="📅",
                font=ctk.CTkFont(size=12)
            ).pack(side="left")
            
            ctk.CTkLabel(
                due_frame,
                text=task.due_date,
                font=ctk.CTkFont(size=12),
                text_color=Theme.TEXT_SECONDARY
            ).pack(side="left", padx=4)
        
        # Tags with professional styling
        if task.tags:
            tags_frame = ctk.CTkFrame(meta_frame, fg_color="transparent")
            tags_frame.pack(side="left")
            
            for tag in task.tags:
                ctk.CTkLabel(
                    tags_frame,
                    text=tag,
                    font=ctk.CTkFont(size=11),
                    text_color=Theme.TEXT_SECONDARY,
                    padx=6,
                    pady=2,
                    corner_radius=4,
                    fg_color=Theme.HOVER
                ).pack(side="left", padx=(0, 4))
        
        # Action buttons with professional styling
        action_frame = ctk.CTkFrame(self, fg_color="transparent")
        action_frame.grid(row=0, column=2, padx=16, pady=16, sticky="ne")
        
        # Pin button
        pin_btn = ctk.CTkButton(
            action_frame,
            text="📌" if task.pinned else "📍",
            width=32,
            height=32,
            corner_radius=16,
            fg_color="transparent",
            hover_color=Theme.HOVER,
            font=ctk.CTkFont(size=14),
            command=lambda: self.on_action("pin", task)
        )
        pin_btn.pack(side="left", padx=(0, 8))
        
        # Edit button
        edit_btn = ctk.CTkButton(
            action_frame,
            text="✏️",
            width=32,
            height=32,
            corner_radius=16,
            fg_color="transparent",
            hover_color=Theme.HOVER,
            font=ctk.CTkFont(size=14),
            command=lambda: self.on_action("edit", task)
        )
        edit_btn.pack(side="left", padx=(0, 8))
        
        # Delete button
        delete_btn = ctk.CTkButton(
            action_frame,
            text="🗑️",
            width=32,
            height=32,
            corner_radius=16,
            fg_color="transparent",
            hover_color="#f44336",
            font=ctk.CTkFont(size=14),
            command=lambda: self.on_action("delete", task)
        )
        delete_btn.pack(side="left")
        
        # Update UI based on completion
        self.update_completion_ui()
    
    def toggle_complete(self):
        self.on_action("complete", self.task)
    
    def update_completion_ui(self):
        if self.task.completed:
            self.title_label.configure(
                font=ctk.CTkFont(size=15, weight="bold", overstrike=True),
                text_color=Theme.TEXT_SECONDARY
            )
            self.desc_label.configure(text_color=Theme.TEXT_SECONDARY)
            self.configure(border_color=Theme.BORDER)
        else:
            self.title_label.configure(
                font=ctk.CTkFont(size=15, weight="bold", overstrike=False),
                text_color=Theme.TEXT
            )
            self.desc_label.configure(text_color=Theme.TEXT_SECONDARY)
