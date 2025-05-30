import customtkinter as ctk
import tkinter as tk
from datetime import datetime, timedelta
from utils.theme import Theme

class DatePicker(ctk.CTkToplevel):
    def __init__(self, parent, initial_date=None):
        super().__init__(parent)
        self.parent = parent
        self.title("Select Date")
        self.geometry("350x400")
        self.resizable(False, False)
        self.configure(fg_color=Theme.BG)
        
        # Bring dialog to front
        self.lift()
        self.attributes('-topmost', True)
        self.after(100, lambda: self.attributes('-topmost', False))
        self.focus_set()
        
        # Parse initial date
        if initial_date:
            try:
                self.selected_date = datetime.strptime(initial_date, "%Y-%m-%d")
            except ValueError:
                self.selected_date = datetime.now()
        else:
            self.selected_date = datetime.now()
            
        self.current_date = self.selected_date
        
        # Header with professional styling
        header_frame = ctk.CTkFrame(self, fg_color=Theme.HEADER, height=50)
        header_frame.pack(fill="x")
        
        # Month and year selection
        control_frame = ctk.CTkFrame(self, fg_color="transparent", height=40)
        control_frame.pack(fill="x", padx=20, pady=(10, 0))
        control_frame.grid_columnconfigure(0, weight=1)
        control_frame.grid_columnconfigure(1, weight=1)
        
        # Month dropdown
        months = ["January", "February", "March", "April", "May", "June",
                 "July", "August", "September", "October", "November", "December"]
        self.month_var = ctk.StringVar(value=months[self.current_date.month - 1])
        self.month_menu = ctk.CTkOptionMenu(
            control_frame,
            values=months,
            variable=self.month_var,
            command=self.month_changed,
            fg_color=Theme.CARD,
            button_color=Theme.ACCENT,
            button_hover_color=Theme.ACCENT_HOVER,
            dropdown_fg_color=Theme.CARD,
            dropdown_hover_color=Theme.HOVER,
            dropdown_text_color=Theme.TEXT
        )
        self.month_menu.grid(row=0, column=0, padx=(0, 10), sticky="ew")
        
        # Year dropdown
        current_year = datetime.now().year
        years = [str(year) for year in range(current_year - 10, current_year + 11)]
        self.year_var = ctk.StringVar(value=str(self.current_date.year))
        self.year_menu = ctk.CTkOptionMenu(
            control_frame,
            values=years,
            variable=self.year_var,
            command=self.year_changed,
            fg_color=Theme.CARD,
            button_color=Theme.ACCENT,
            button_hover_color=Theme.ACCENT_HOVER,
            dropdown_fg_color=Theme.CARD,
            dropdown_hover_color=Theme.HOVER,
            dropdown_text_color=Theme.TEXT
        )
        self.year_menu.grid(row=0, column=1, sticky="ew")
        
        # Navigation buttons
        nav_frame = ctk.CTkFrame(self, fg_color="transparent", height=30)
        nav_frame.pack(fill="x", padx=20, pady=(5, 0))
        
        self.prev_btn = ctk.CTkButton(
            nav_frame, 
            text="◀",
            width=30,
            height=30,
            corner_radius=15,
            fg_color="transparent",
            hover_color=Theme.HOVER,
            command=self.prev_month
        )
        self.prev_btn.pack(side="left")
        
        self.month_label = ctk.CTkLabel(
            nav_frame, 
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=Theme.TEXT
        )
        self.month_label.pack(side="left", expand=True)
        
        self.next_btn = ctk.CTkButton(
            nav_frame, 
            text="▶",
            width=30,
            height=30,
            corner_radius=15,
            fg_color="transparent",
            hover_color=Theme.HOVER,
            command=self.next_month
        )
        self.next_btn.pack(side="right")
        
        # Calendar grid
        self.grid_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.grid_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Weekday headers
        weekdays = ["SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT"]
        for i, day in enumerate(weekdays):
            label = ctk.CTkLabel(
                self.grid_frame, 
                text=day, 
                width=40,
                height=30,
                font=ctk.CTkFont(size=11, weight="bold"),
                text_color=Theme.TEXT_SECONDARY
            )
            label.grid(row=0, column=i, padx=2, pady=(0, 5))
        
        self.day_buttons = []
        self.update_calendar()
        
        # Action buttons
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        today_btn = ctk.CTkButton(
            button_frame,
            text="Today",
            width=100,
            height=35,
            fg_color=Theme.ACCENT,
            hover_color=Theme.ACCENT_HOVER,
            command=self.select_today
        )
        today_btn.pack(side="left")
        
        cancel_btn = ctk.CTkButton(
            button_frame,
            text="Cancel",
            width=100,
            height=35,
            fg_color="transparent",
            border_width=1,
            border_color=Theme.BORDER,
            text_color=Theme.TEXT,
            command=self.destroy
        )
        cancel_btn.pack(side="right")
        
        self.grab_set()
        self.transient(self.parent)
        self.wait_window()
    
    def month_changed(self, choice):
        months = ["January", "February", "March", "April", "May", "June",
                 "July", "August", "September", "October", "November", "December"]
        month_index = months.index(choice) + 1
        self.current_date = self.current_date.replace(month=month_index)
        self.update_calendar()
    
    def year_changed(self, choice):
        self.current_date = self.current_date.replace(year=int(choice))
        self.update_calendar()
    
    def select_today(self):
        today = datetime.now()
        self.selected_date = today
        self.current_date = today
        self.month_var.set(self.current_date.strftime("%B"))
        self.year_var.set(str(self.current_date.year))
        self.update_calendar()
        self.destroy()
    
    def prev_month(self):
        self.current_date = self.current_date.replace(day=1) - timedelta(days=1)
        self.month_var.set(self.current_date.strftime("%B"))
        self.year_var.set(str(self.current_date.year))
        self.update_calendar()
    
    def next_month(self):
        next_month = self.current_date.replace(day=28) + timedelta(days=4)
        self.current_date = next_month.replace(day=1)
        self.month_var.set(self.current_date.strftime("%B"))
        self.year_var.set(str(self.current_date.year))
        self.update_calendar()
    
    def update_calendar(self):
        self.month_label.configure(text=self.current_date.strftime("%B %Y"))
        
        # Clear existing buttons
        for btn in self.day_buttons:
            btn.destroy()
        self.day_buttons = []
        
        # Get first day of month and days in month
        first_day = self.current_date.replace(day=1)
        days_in_month = (first_day.replace(month=first_day.month % 12 + 1, day=1) - 
                         timedelta(days=1)).day
        
        # Create day buttons
        row = 1
        col = first_day.weekday()
        
        for day in range(1, days_in_month + 1):
            btn = ctk.CTkButton(
                self.grid_frame,
                text=str(day),
                width=40,
                height=40,
                corner_radius=20,
                fg_color=Theme.BG,
                hover_color=Theme.HOVER,
                text_color=Theme.TEXT,
                command=lambda d=day: self.select_date(d),
                font=ctk.CTkFont(size=14)
            )
            btn.grid(row=row, column=col, padx=2, pady=2)
            self.day_buttons.append(btn)
            
            # Highlight current day
            today = datetime.now()
            if (self.current_date.year == today.year and 
                self.current_date.month == today.month and 
                day == today.day):
                btn.configure(fg_color=Theme.ACCENT, text_color="white")
            
            # Highlight selected day
            if (self.current_date.year == self.selected_date.year and
                self.current_date.month == self.selected_date.month and
                day == self.selected_date.day):
                btn.configure(fg_color=Theme.ACCENT_HOVER, text_color="white")
            
            col += 1
            if col > 6:
                col = 0
                row += 1
    
    def select_date(self, day):
        self.selected_date = self.current_date.replace(day=day)
        self.destroy()
