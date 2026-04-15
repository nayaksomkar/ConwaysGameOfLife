"""
Screenshot utility for capturing game states.
"""

import os
from datetime import datetime
from pathlib import Path
import pygame


def capture_screenshot(screen: pygame.Surface, folder: str = "assets/screenshots") -> str:
    """
    Capture a screenshot of the current game state.
    
    Args:
        screen: Pygame surface to capture
        folder: Folder to save screenshots
        
    Returns:
        Path to saved screenshot
    """
    Path(folder).mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"conway_gol_{timestamp}.png"
    filepath = os.path.join(folder, filename)
    
    pygame.image.save(screen, filepath)
    
    return filepath