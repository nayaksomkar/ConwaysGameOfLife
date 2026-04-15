"""
Tests for the Rules module.
"""

import pytest
import numpy as np
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.game.rules import Rules


class TestRules:
    def test_count_neighbors_center(self):
        """Test neighbor counting for center cell"""
        cells = np.array([
            [0, 0, 0],
            [0, 1, 0],
            [0, 0, 0]
        ])
        assert Rules.count_neighbors(cells, 1, 1) == 0
    
    def test_count_neighbors_all_alive(self):
        """Test neighbor counting when all 8 neighbors are alive"""
        cells = np.array([
            [1, 1, 1],
            [1, 0, 1],
            [1, 1, 1]
        ])
        assert Rules.count_neighbors(cells, 1, 1) == 8
    
    def test_count_neighbors_partial(self):
        """Test neighbor counting with some alive neighbors"""
        cells = np.array([
            [1, 0, 1],
            [0, 1, 0],
            [1, 0, 1]
        ])
        assert Rules.count_neighbors(cells, 1, 1) == 4
    
    def test_count_neighbors_corner(self):
        """Test neighbor counting at corner"""
        cells = np.array([
            [1, 1, 0],
            [1, 0, 0],
            [0, 0, 0]
        ])
        assert Rules.count_neighbors(cells, 0, 0) == 2
    
    def test_compute_next_state_alive_survives_2(self):
        """Test alive cell with 2 neighbors survives"""
        assert Rules.compute_next_state(1, 2) == 1
    
    def test_compute_next_state_alive_survives_3(self):
        """Test alive cell with 3 neighbors survives"""
        assert Rules.compute_next_state(1, 3) == 1
    
    def test_compute_next_state_alive_dies_underpopulation(self):
        """Test alive cell with less than 2 neighbors dies"""
        assert Rules.compute_next_state(1, 0) == 0
        assert Rules.compute_next_state(1, 1) == 0
    
    def test_compute_next_state_alive_dies_overpopulation(self):
        """Test alive cell with more than 3 neighbors dies"""
        assert Rules.compute_next_state(1, 4) == 0
    
    def test_compute_next_state_dead_becomes_alive(self):
        """Test dead cell with exactly 3 neighbors becomes alive"""
        assert Rules.compute_next_state(0, 3) == 1
    
    def test_compute_next_state_dead_stays_dead(self):
        """Test dead cell with not exactly 3 neighbors stays dead"""
        assert Rules.compute_next_state(0, 0) == 0
        assert Rules.compute_next_state(0, 1) == 0
        assert Rules.compute_next_state(0, 2) == 0
        assert Rules.compute_next_state(0, 4) == 0
    
    def test_update_grid_stable_pattern(self):
        """Test grid update with stable blinker pattern"""
        cells = np.array([
            [0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0]
        ])
        new_cells = Rules.update_grid(cells)
        expected = np.array([
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 1, 1, 1, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0]
        ])
        assert np.array_equal(new_cells, expected)
    
    def test_is_stable_same(self):
        """Test stability check when grids are equal"""
        cells = np.array([[1, 0], [0, 1]])
        assert Rules.is_stable(cells, cells) is True
    
    def test_is_stable_different(self):
        """Test stability check when grids differ"""
        cells1 = np.array([[1, 0], [0, 1]])
        cells2 = np.array([[0, 1], [1, 0]])
        assert Rules.is_stable(cells1, cells2) is False
    
    def test_count_population(self):
        """Test population counting"""
        cells = np.array([
            [1, 0, 1],
            [0, 1, 0],
            [1, 0, 1]
        ])
        assert Rules.count_population(cells) == 5