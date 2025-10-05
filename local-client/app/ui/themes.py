from dataclasses import dataclass
from typing import Dict, Tuple

@dataclass
class ColorScheme:
    primary: str
    secondary: str
    background: str
    surface: str
    text_primary: str
    text_secondary: str
    success: str
    warning: str
    error: str

@dataclass
class AppTheme:
    colors: ColorScheme
    fonts: Dict[str, Tuple[str, int]]
    spacing: Dict[str, int]

class ThemeManager:
    """Менеджер тем приложения"""
    
    DARK_THEME = AppTheme(
        colors=ColorScheme(
            primary="#00D4AA",
            secondary="#00B894",
            background="#0A0A0A",
            surface="#1A1A1A",
            text_primary="#FFFFFF",
            text_secondary="#888888",
            success="#00D4AA",
            warning="#FFA726",
            error="#FF6B6B"
        ),
        fonts={
            "title": ("Arial", 24, "bold"),
            "subtitle": ("Arial", 16),
            "body": ("Arial", 12),
            "button": ("Arial", 11, "bold"),
            "caption": ("Arial", 10)
        },
        spacing={
            "xs": 5,
            "sm": 10,
            "md": 20,
            "lg": 30,
            "xl": 40
        }
    )
    
    @classmethod
    def get_theme(cls) -> AppTheme:
        return cls.DARK_THEME