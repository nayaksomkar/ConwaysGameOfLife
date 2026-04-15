"""
Grid module for Conway's Game of Life
Manages the cell grid and its operations.
"""

import numpy as np
from typing import Tuple, Optional


class Grid:
    def __init__(self, cols: int, rows: int, cell_size: int = 10):
        self.cols = cols
        self.rows = rows
        self.cell_size = cell_size
        self.cells = np.zeros((rows, cols), dtype=np.int8)
    
    def clear(self):
        """Clear all cells"""
        self.cells.fill(0)
    
    def randomize(self, density: float = 0.3):
        """Randomize cell states"""
        self.cells = np.random.choice(
            [0, 1], 
            size=(self.rows, self.cols), 
            p=[1 - density, density]
        )
    
    def set_cell(self, row: int, col: int, value: int):
        """Set a specific cell value"""
        if 0 <= row < self.rows and 0 <= col < self.cols:
            self.cells[row, col] = value
    
    def toggle_cell(self, row: int, col: int):
        """Toggle a cell's state"""
        if 0 <= row < self.rows and 0 <= col < self.cols:
            self.cells[row, col] = 1 - self.cells[row, col]
    
    def get_cell(self, row: int, col: int) -> int:
        """Get a cell's value"""
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return self.cells[row, col]
        return 0
    
    def set_pattern(self, start_row: int, start_col: int, pattern: np.ndarray):
        """Set a pattern of cells"""
        for i in range(pattern.shape[0]):
            for j in range(pattern.shape[1]):
                row = start_row + i
                col = start_col + j
                if 0 <= row < self.rows and 0 <= col < self.cols:
                    self.cells[row, col] = pattern[i, j]
    
    def update(self, with_progress: bool = False):
        """Update the grid to the next generation"""
        new_cells = np.zeros((self.rows, self.cols), dtype=np.int8)
        
        for row in range(self.rows):
            for col in range(self.cols):
                alive_neighbors = self._count_neighbors(row, col)
                current_state = self.cells[row, col]
                
                if current_state == 1:
                    if 2 <= alive_neighbors <= 3:
                        new_cells[row, col] = 1
                else:
                    if alive_neighbors == 3:
                        new_cells[row, col] = 1
        
        self.cells = new_cells
    
    def _count_neighbors(self, row: int, col: int) -> int:
        """Count alive neighbors around a cell"""
        count = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                neighbor_row = row + i
                neighbor_col = col + j
                if 0 <= neighbor_row < self.rows and 0 <= neighbor_col < self.cols:
                    count += self.cells[neighbor_row, neighbor_col]
        return count
    
    @property
    def population(self) -> int:
        """Get the current population count"""
        return int(np.sum(self.cells))
    
    @property
    def shape(self) -> Tuple[int, int]:
        """Get grid dimensions"""
        return (self.rows, self.cols)