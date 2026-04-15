"""
Rules module for Conway's Game of Life
Implements the game rules and neighbor counting.
"""

import numpy as np
from typing import Optional


class Rules:
    @staticmethod
    def count_neighbors(cells: np.ndarray, row: int, col: int) -> int:
        """
        Count alive neighbors around a cell using numpy slicing.
        Handles edge cases (wrap-around for toroidal grid).
        """
        rows, cols = cells.shape
        
        neighbor_sum = 0
        
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                    
                neighbor_row = (row + i + rows) % rows
                neighbor_col = (col + j + cols) % cols
                
                neighbor_sum += cells[neighbor_row, neighbor_col]
        
        return int(neighbor_sum)
    
    @staticmethod
    def compute_next_state(current_state: int, neighbors: int) -> int:
        """
        Compute the next state based on Conway's rules.
        
        Rules:
        - Alive cell (1) with 2-3 neighbors survives (stays 1)
        - Alive cell with <2 or >3 neighbors dies (becomes 0)
        - Dead cell (0) with exactly 3 neighbors becomes alive (becomes 1)
        - All other dead cells stay dead (stays 0)
        """
        if current_state == 1:
            return 1 if 2 <= neighbors <= 3 else 0
        else:
            return 1 if neighbors == 3 else 0
    
    @staticmethod
    def update_grid(cells: np.ndarray) -> np.ndarray:
        """
        Update entire grid to next generation.
        Uses numpy for efficient computation.
        """
        rows, cols = cells.shape
        new_cells = np.zeros((rows, cols), dtype=cells.dtype)
        
        for row in range(rows):
            for col in range(cols):
                neighbors = Rules.count_neighbors(cells, row, col)
                new_cells[row, col] = Rules.compute_next_state(
                    cells[row, col], 
                    neighbors
                )
        
        return new_cells
    
    @staticmethod
    def is_stable(cells: np.ndarray, prev_cells: Optional[np.ndarray] = None) -> bool:
        """
        Check if the grid has reached a stable state.
        """
        if prev_cells is None:
            return False
        
        return np.array_equal(cells, prev_cells)
    
    @staticmethod
    def count_population(cells: np.ndarray) -> int:
        """Count total alive cells."""
        return int(np.sum(cells))