class Theme:
    # Dark Theme
    DARK_BG = "#0f1117"
    DARK_CARD = "#1b1f2d"
    DARK_HEADER = "#161925"
    DARK_ACCENT = "#5c6bff"
    DARK_ACCENT_HOVER = "#4755d8"
    DARK_TEXT = "#f4f6ff"
    DARK_TEXT_SECONDARY = "#9faac2"
    DARK_BORDER = "#262c3e"
    DARK_HOVER = "#1f2534"
    DARK_MENU = "#1b1f2d"
    DARK_TAG_BG = "#2c3361"
    
    # Light Theme
    LIGHT_BG = "#f4f6fb"
    LIGHT_CARD = "#ffffff"
    LIGHT_HEADER = "#e3e7f3"
    LIGHT_ACCENT = "#4d5dff"
    LIGHT_ACCENT_HOVER = "#3a47d6"
    LIGHT_TEXT = "#1a2132"
    LIGHT_TEXT_SECONDARY = "#5a6275"
    LIGHT_BORDER = "#d7ddee"
    LIGHT_HOVER = "#eef1fb"
    LIGHT_MENU = "#ffffff"
    LIGHT_TAG_BG = "#dfe3ff"
    
    # Current theme (dark by default)
    BG = DARK_BG
    CARD = DARK_CARD
    HEADER = DARK_HEADER
    ACCENT = DARK_ACCENT
    ACCENT_HOVER = DARK_ACCENT_HOVER
    TEXT = DARK_TEXT
    TEXT_SECONDARY = DARK_TEXT_SECONDARY
    BORDER = DARK_BORDER
    HOVER = DARK_HOVER
    MENU = DARK_MENU
    TAG_BG = DARK_TAG_BG
    MODE = "dark"
    
    # Dimensions
    CORNER_RADIUS = 8
    CARD_PADDING = 12
    
    @staticmethod
    def toggle_theme():
        new_mode = "light" if Theme.MODE == "dark" else "dark"
        Theme.set_theme(new_mode)
    
    @staticmethod
    def set_theme(mode: str):
        normalized = mode.lower()
        if normalized == "light":
            Theme.MODE = "light"
            Theme.BG = Theme.LIGHT_BG
            Theme.CARD = Theme.LIGHT_CARD
            Theme.HEADER = Theme.LIGHT_HEADER
            Theme.ACCENT = Theme.LIGHT_ACCENT
            Theme.ACCENT_HOVER = Theme.LIGHT_ACCENT_HOVER
            Theme.TEXT = Theme.LIGHT_TEXT
            Theme.TEXT_SECONDARY = Theme.LIGHT_TEXT_SECONDARY
            Theme.BORDER = Theme.LIGHT_BORDER
            Theme.HOVER = Theme.LIGHT_HOVER
            Theme.MENU = Theme.LIGHT_MENU
            Theme.TAG_BG = Theme.LIGHT_TAG_BG
        else:
            Theme.MODE = "dark"
            Theme.BG = Theme.DARK_BG
            Theme.CARD = Theme.DARK_CARD
            Theme.HEADER = Theme.DARK_HEADER
            Theme.ACCENT = Theme.DARK_ACCENT
            Theme.ACCENT_HOVER = Theme.DARK_ACCENT_HOVER
            Theme.TEXT = Theme.DARK_TEXT
            Theme.TEXT_SECONDARY = Theme.DARK_TEXT_SECONDARY
            Theme.BORDER = Theme.DARK_BORDER
            Theme.HOVER = Theme.DARK_HOVER
            Theme.MENU = Theme.DARK_MENU
            Theme.TAG_BG = Theme.DARK_TAG_BG
    
    @staticmethod
    def get_theme_path():
        return "dark-blue"
