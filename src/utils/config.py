"""
Configuration module for Conway's Game of Life
Contains all configurable parameters and settings.
"""


class Config:
    def __init__(self):
        self.CELL_SIZE = 10
        self.COLS = 80
        self.ROWS = 60
        self.WINDOW_WIDTH = 800
        self.WINDOW_HEIGHT = 600
        self.FPS = 60
        
        self.COLOR_BG = (10, 10, 10)
        self.COLOR_GRID = (40, 40, 40)
        self.COLOR_ALIVE = (255, 255, 255)
        self.COLOR_DYING = (170, 170, 170)
        self.COLOR_BORN = (0, 255, 0)
        
        self.RANDOM_DENSITY = 0.3
        
    def update_dimensions(self, width, height):
        self.COLS = width // self.CELL_SIZE
        self.ROWS = height // self.CELL_SIZE
    
    def __setattr__(self, name, value):
        super().__setattr__(name, value)