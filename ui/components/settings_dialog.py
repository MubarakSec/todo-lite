import customtkinter as ctk
from utils.theme import Theme

class SettingsDialog(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Settings")
        self.geometry("500x400")
        self.resizable(False, False)
        self.configure(fg_color=Theme.BG)
        
        # Professional header
        header_frame = ctk.CTkFrame(self, fg_color=Theme.HEADER, height=50, corner_radius=0)
        header_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(
            header_frame,
            text="APPLICATION SETTINGS",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=Theme.TEXT
        ).pack(side="left", padx=20)
        
        # Main content
        content_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Theme selection
        ctk.CTkLabel(
            content_frame, 
            text="Appearance",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=Theme.TEXT
        ).pack(anchor="w", pady=(0, 15))
        
        theme_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        theme_frame.pack(fill="x", padx=10)
        
        self.theme_var = ctk.StringVar(value="dark")
        themes = [("Dark Mode", "dark"), ("Light Mode", "light")]
        
        for text, value in themes:
            btn = ctk.CTkRadioButton(
                theme_frame,
                text=text,
                variable=self.theme_var,
                value=value,
                text_color=Theme.TEXT,
                command=self.change_theme
            )
            btn.pack(side="left", padx=(0, 20))
        
        # Accent color
        ctk.CTkLabel(
            content_frame, 
            text="Accent Color",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=Theme.TEXT
        ).pack(anchor="w", pady=(20, 10))
        
        colors_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        colors_frame.pack(fill="x", padx=10, pady=(0, 20))
        
        colors = ["#2962ff", "#00bcd4", "#4caf50", "#ff9800", "#e91e63"]
        for color in colors:
            btn = ctk.CTkButton(
                colors_frame,
                text="",
                width=40,
                height=40,
                corner_radius=20,
                fg_color=color,
                hover_color=color,
                border_width=2,
                border_color="#ffffff" if Theme.BG == Theme.DARK_BG else "#000000",
                command=lambda c=color: self.change_accent(c)
            )
            btn.pack(side="left", padx=(0, 10))
        
        # Save button
        button_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        button_frame.pack(fill="x", pady=(20, 0))
        
        save_btn = ctk.CTkButton(
            button_frame,
            text="Apply Settings",
            height=45,
            fg_color=Theme.ACCENT,
            hover_color=Theme.ACCENT_HOVER,
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self.destroy
        )
        save_btn.pack(side="right")
    
    def change_theme(self):
        theme = self.theme_var.get()
        Theme.set_theme(theme)
        self.configure(fg_color=Theme.BG)
    
    def change_accent(self, color):
        Theme.ACCENT = color
        # Create a slightly darker version for hover
        r, g, b = [int(color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4)]
        hover_r = max(0, r - 30)
        hover_g = max(0, g - 30)
        hover_b = max(0, b - 30)
        Theme.ACCENT_HOVER = f"#{hover_r:02x}{hover_g:02x}{hover_b:02x}"
