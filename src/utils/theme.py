"""
Modern UI Theme Manager for Conway's Game of Life
Contains modern, visually stunning themes with smooth gradients and effects.
"""

from typing import Dict, List


class ThemeManager:
    def __init__(self):
        self._themes = {
            "cyberpunk": {
                "name": "Cyberpunk",
                "background": (8, 8, 20),
                "grid_line": (25, 25, 50),
                "cell_alive": (0, 255, 255),
                "cell_dying": (255, 0, 128),
                "cell_born": (255, 255, 0),
                "glow_alive": (0, 200, 200),
                "glow_dying": (200, 0, 100),
                "glow_born": (200, 200, 0),
                "ui_bg": (15, 15, 35, 230),
                "ui_border": (0, 180, 200),
                "text_primary": (0, 255, 255),
                "text_secondary": (100, 150, 170),
                "accent": (255, 0, 128),
            },
            "nebula": {
                "name": "Nebula",
                "background": (5, 5, 15),
                "grid_line": (30, 20, 45),
                "cell_alive": (138, 43, 226),
                "cell_dying": (255, 100, 150),
                "cell_born": (100, 200, 255),
                "glow_alive": (138, 43, 226),
                "glow_dying": (200, 80, 120),
                "glow_born": (80, 180, 220),
                "ui_bg": (20, 15, 35, 230),
                "ui_border": (138, 43, 226),
                "text_primary": (180, 140, 255),
                "text_secondary": (120, 100, 150),
                "accent": (255, 100, 200),
            },
            "arctic": {
                "name": "Arctic",
                "background": (10, 15, 25),
                "grid_line": (30, 45, 60),
                "cell_alive": (150, 230, 255),
                "cell_dying": (100, 180, 220),
                "cell_born": (200, 255, 200),
                "glow_alive": (120, 200, 230),
                "glow_dying": (80, 150, 190),
                "glow_born": (170, 230, 180),
                "ui_bg": (20, 30, 45, 230),
                "ui_border": (100, 180, 220),
                "text_primary": (180, 220, 255),
                "text_secondary": (120, 150, 180),
                "accent": (100, 200, 255),
            },
            "inferno": {
                "name": "Inferno",
                "background": (15, 5, 5),
                "grid_line": (45, 20, 15),
                "cell_alive": (255, 180, 50),
                "cell_dying": (255, 80, 20),
                "cell_born": (255, 255, 150),
                "glow_alive": (255, 150, 30),
                "glow_dying": (220, 60, 10),
                "glow_born": (230, 220, 100),
                "ui_bg": (30, 15, 10, 230),
                "ui_border": (255, 150, 50),
                "text_primary": (255, 200, 100),
                "text_secondary": (180, 100, 50),
                "accent": (255, 100, 30),
            },
            "emerald": {
                "name": "Emerald",
                "background": (5, 20, 15),
                "grid_line": (20, 50, 35),
                "cell_alive": (50, 255, 150),
                "cell_dying": (150, 200, 100),
                "cell_born": (150, 255, 200),
                "glow_alive": (30, 220, 120),
                "glow_dying": (120, 170, 80),
                "glow_born": (120, 230, 170),
                "ui_bg": (15, 35, 25, 230),
                "ui_border": (50, 220, 130),
                "text_primary": (100, 255, 180),
                "text_secondary": (80, 170, 120),
                "accent": (50, 255, 150),
            },
            "violet": {
                "name": "Violet",
                "background": (15, 10, 25),
                "grid_line": (40, 30, 50),
                "cell_alive": (220, 100, 255),
                "cell_dying": (180, 50, 200),
                "cell_born": (255, 180, 255),
                "glow_alive": (190, 80, 230),
                "glow_dying": (150, 40, 170),
                "glow_born": (230, 150, 230),
                "ui_bg": (25, 18, 40, 230),
                "ui_border": (200, 90, 230),
                "text_primary": (230, 180, 255),
                "text_secondary": (150, 110, 180),
                "accent": (255, 100, 255),
            },
            "midnight": {
                "name": "Midnight",
                "background": (5, 5, 12),
                "grid_line": (25, 25, 40),
                "cell_alive": (200, 220, 255),
                "cell_dying": (120, 140, 180),
                "cell_born": (255, 255, 200),
                "glow_alive": (170, 190, 230),
                "glow_dying": (100, 120, 160),
                "glow_born": (230, 230, 180),
                "ui_bg": (12, 12, 25, 230),
                "ui_border": (150, 170, 200),
                "text_primary": (200, 220, 255),
                "text_secondary": (130, 150, 180),
                "accent": (150, 180, 255),
            },
            "sunset": {
                "name": "Sunset",
                "background": (20, 10, 15),
                "grid_line": (50, 30, 35),
                "cell_alive": (255, 150, 80),
                "cell_dying": (255, 80, 60),
                "cell_born": (255, 220, 120),
                "glow_alive": (230, 130, 70),
                "glow_dying": (220, 60, 40),
                "glow_born": (230, 200, 100),
                "ui_bg": (35, 20, 25, 230),
                "ui_border": (255, 150, 80),
                "text_primary": (255, 200, 150),
                "text_secondary": (180, 110, 90),
                "accent": (255, 120, 80),
            },
        }
    
    def get_theme(self, name: str) -> Dict:
        return self._themes.get(name, self._themes["cyberpunk"])
    
    def get_all_themes(self) -> Dict:
        return self._themes
    
    def get_theme_names(self) -> List[str]:
        return list(self._themes.keys())