"""
Tests for the Grid module.
"""

import pytest
import numpy as np
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.game.grid import Grid


class TestGrid:
    def test_init(self):
        """Test grid initialization"""
        grid = Grid(10, 20, 5)
        assert grid.cols == 10
        assert grid.rows == 20
        assert grid.cell_size == 5
        assert grid.cells.shape == (20, 10)
    
    def test_clear(self):
        """Test clearing the grid"""
        grid = Grid(5, 5)
        grid.cells[2, 2] = 1
        grid.clear()
        assert np.sum(grid.cells) == 0
    
    def test_set_cell(self):
        """Test setting a cell value"""
        grid = Grid(10, 10)
        grid.set_cell(5, 5, 1)
        assert grid.cells[5, 5] == 1
    
    def test_toggle_cell(self):
        """Test toggling a cell"""
        grid = Grid(10, 10)
        grid.toggle_cell(5, 5)
        assert grid.cells[5, 5] == 1
        grid.toggle_cell(5, 5)
        assert grid.cells[5, 5] == 0
    
    def test_get_cell(self):
        """Test getting a cell value"""
        grid = Grid(10, 10)
        grid.set_cell(3, 7, 1)
        assert grid.get_cell(3, 7) == 1
        assert grid.get_cell(0, 0) == 0
    
    def test_randomize(self):
        """Test randomizing the grid"""
        grid = Grid(100, 100)
        grid.randomize(density=0.5)
        population = np.sum(grid.cells)
        assert 4000 < population < 6000
    
    def test_set_pattern(self):
        """Test setting a pattern"""
        grid = Grid(10, 10)
        pattern = np.array([[1, 1], [1, 0]])
        grid.set_pattern(0, 0, pattern)
        assert grid.cells[0, 0] == 1
        assert grid.cells[0, 1] == 1
        assert grid.cells[1, 0] == 1
        assert grid.cells[1, 1] == 0
    
    def test_update_blinker(self):
        """Test updating grid with blinker pattern"""
        grid = Grid(5, 5)
        grid.set_pattern(1, 2, np.array([[1], [1], [1]]))
        grid.update()
        expected = np.array([
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 1, 1, 1, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0]
        ])
        assert np.array_equal(grid.cells, expected)
    
    def test_population_property(self):
        """Test population property"""
        grid = Grid(3, 3)
        grid.set_cell(0, 0, 1)
        grid.set_cell(1, 1, 1)
        grid.set_cell(2, 2, 1)
        assert grid.population == 3
    
    def test_shape_property(self):
        """Test shape property"""
        grid = Grid(10, 20)
        assert grid.shape == (20, 10)