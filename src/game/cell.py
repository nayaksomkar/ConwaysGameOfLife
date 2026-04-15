"""
Cell module for Conway's Game of Life
Represents individual cells in the grid.
"""

from typing import Tuple


class Cell:
    def __init__(self, row: int, col: int, alive: bool = False):
        self.row = row
        self.col = col
        self.alive = alive
        self.next_state = False
    
    def __repr__(self):
        return f"Cell({self.row}, {self.col}, {self.alive})"
    
    def is_alive(self) -> bool:
        return self.alive
    
    def set_alive(self, alive: bool):
        self.alive = alive
    
    def get_position(self) -> Tuple[int, int]:
        return (self.row, self.col)
    
    def compute_next_state(self, neighbors: int):
        """
        Compute next state based on Conway's rules:
        - Alive cell with 2-3 neighbors survives
        - Dead cell with exactly 3 neighbors becomes alive
        - All other cells die or stay dead
        """
        if self.alive:
            self.next_state = 2 <= neighbors <= 3
        else:
            self.next_state = neighbors == 3
    
    def apply_next_state(self):
        self.alive = self.next_state