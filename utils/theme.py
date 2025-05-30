class Theme:
    # Dark Theme
    DARK_BG = "#121212"
    DARK_CARD = "#1e1e1e"
    DARK_HEADER = "#1a1a1e"
    DARK_ACCENT = "#2962ff"
    DARK_ACCENT_HOVER = "#0039cb"
    DARK_TEXT = "#e0e0e0"
    DARK_TEXT_SECONDARY = "#9e9e9e"
    DARK_BORDER = "#2d2d2d"
    DARK_HOVER = "#252525"
    DARK_MENU = "#1e1e1e"
    DARK_TAG_BG = "#1e3a8a"
    
    # Light Theme (off-white)
    LIGHT_BG = "#f8f9fa"  # Off-white background
    LIGHT_CARD = "#ffffff"  # Pure white cards
    LIGHT_HEADER = "#e9ecef"  # Light gray header
    LIGHT_ACCENT = "#2962ff"
    LIGHT_ACCENT_HOVER = "#0039cb"
    LIGHT_TEXT = "#393939"  # Dark text
    LIGHT_TEXT_SECONDARY = "#6c757d"  # Medium gray text
    LIGHT_BORDER = "#dee2e6"  # Light border
    LIGHT_HOVER = "#e9ecef"  # Light hover
    LIGHT_MENU = "#ffffff"
    LIGHT_TAG_BG = "#dbeafe"  # Light blue for tags
    
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
    
    # Dimensions
    CORNER_RADIUS = 8
    CARD_PADDING = 12
    
    @staticmethod
    def toggle_theme():
        if Theme.BG == Theme.DARK_BG:
            # Switch to light theme
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
            # Switch to dark theme
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
