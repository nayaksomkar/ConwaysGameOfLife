"""
Conway's Game of Life - Core Game Logic
Simple, modern, adaptive UI with black background and white dots.
"""

import pygame
import numpy as np
import math
import random


class SimpleButton:
    def __init__(self, x, y, width, height, text, callback=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.callback = callback
        self.hovered = False
    
    def update(self, mouse_pos, mouse_pressed):
        self.hovered = self.rect.collidepoint(mouse_pos)
        if mouse_pressed[0] and self.hovered and self.callback:
            self.callback()
    
    def draw(self, screen, font):
        color = (60, 60, 60) if self.hovered else (40, 40, 40)
        pygame.draw.rect(screen, color, self.rect, border_radius=8)
        pygame.draw.rect(screen, (100, 100, 100), self.rect, 1, border_radius=8)
        
        text_surf = font.render(self.text, True, (220, 220, 220))
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)


class SimpleSlider:
    def __init__(self, x, y, width, min_val, max_val, value, label):
        self.x = x
        self.y = y
        self.width = width
        self.height = 20
        self.min_val = min_val
        self.max_val = max_val
        self.value = value
        self.label = label
        self.dragging = False
        self.hovered = False
    
    def update(self, mouse_pos, mouse_pressed):
        rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.hovered = rect.collidepoint(mouse_pos)
        
        if mouse_pressed[self.hovered]:
            self.dragging = True
        
        if not any(mouse_pressed):
            self.dragging = False
        
        if self.dragging:
            ratio = (mouse_pos[0] - self.x) / self.width
            ratio = max(0, min(1, ratio))
            self.value = self.min_val + ratio * (self.max_val - self.min_val)
    
    def draw(self, screen, font):
        label_surf = font.render(f"{self.label}: {int(self.value)}", True, (180, 180, 180))
        screen.blit(label_surf, (self.x, self.y - 16))
        
        pygame.draw.rect(screen, (30, 30, 30), (self.x, self.y + 6, self.width, 8), border_radius=4)
        
        ratio = (self.value - self.min_val) / (self.max_val - self.min_val)
        fill_width = int(self.width * ratio)
        pygame.draw.rect(screen, (200, 200, 200), (self.x, self.y + 6, fill_width, 8), border_radius=4)
        
        knob_x = self.x + fill_width
        pygame.draw.circle(screen, (255, 255, 255), (knob_x, self.y + 10), 8)


class CellColor:
    COLORS = [
        (255, 255, 255),  # White
        (255, 100, 100),  # Red
        (100, 255, 100),  # Green
        (100, 100, 255),  # Blue
        (255, 255, 100),  # Yellow
        (255, 100, 255),  # Magenta
        (100, 255, 255),  # Cyan
        (255, 180, 100),  # Orange
    ]
    MAX_COLORS = 8
    
    @classmethod
    def get_color(cls, index):
        return cls.COLORS[index % cls.MAX_COLORS]
    
    @classmethod
    def set_max_colors(cls, count):
        cls.MAX_COLORS = max(1, min(count, len(cls.COLORS)))
    
    @classmethod
    def get_available_colors(cls):
        return cls.COLORS[:cls.MAX_COLORS]


class AdaptiveUI:
    def __init__(self):
        self.buttons = []
        self.sliders = []
        self.compact_mode = False
    
    def create_elements(self, screen_width, screen_height):
        self.buttons = []
        self.sliders = []
        
        if screen_width < 900:
            self.compact_mode = True
            self._create_compact_layout(screen_width, screen_height)
        else:
            self.compact_mode = False
            self._create_full_layout()
    
    def _create_full_layout(self):
        panel_x = 20
        panel_y = 20
        
        buttons = [
            (panel_x, panel_y, "Random"),
            (panel_x + 80, panel_y, "Play"),
            (panel_x, panel_y + 40, "Clear"),
            (panel_x + 80, panel_y + 40, "Slow"),
            (panel_x, panel_y + 80, "Fast"),
            (panel_x + 80, panel_y + 80, "Grid"),
        ]
        
        for x, y, text in buttons:
            self.buttons.append(SimpleButton(x, y, 70, 30, text))
        
        self.sliders = [
            SimpleSlider(panel_x, panel_y + 125, 150, 1, 120, 60, "Speed"),
            SimpleSlider(panel_x, panel_y + 160, 150, 1, 8, 8, "Colors"),
        ]
    
    def _create_compact_layout(self, screen_width, screen_height):
        row_width = screen_width - 40
        btn_width = (row_width - 25) // 4
        
        y_pos = 20
        row1 = ["Random", "Play", "Clear", "Slow"]
        for i, text in enumerate(row1):
            self.buttons.append(SimpleButton(20 + i * (btn_width + 5), y_pos, btn_width, 28, text))
        
        y_pos += 38
        row2 = ["Fast", "Grid"]
        for i, text in enumerate(row2):
            self.buttons.append(SimpleButton(20 + i * (btn_width + 5), y_pos, btn_width, 28, text))
        
        y_pos += 40
        self.sliders = [
            SimpleSlider(20, y_pos, row_width - 20, 1, 120, 60, "Speed"),
            SimpleSlider(20, y_pos + 35, row_width - 20, 1, 8, 8, "Colors"),
        ]
    
    def draw(self, screen, game, font, small_font):
        if not self.compact_mode:
            panel_rect = pygame.Rect(10, 10, 170, 280)
            s = pygame.Surface((170, 280), pygame.SRCALPHA)
            s.fill((20, 20, 20, 220))
            screen.blit(s, (10, 10))
            pygame.draw.rect(screen, (80, 80, 80), panel_rect, 1, border_radius=12)
        
        for button in self.buttons:
            button.draw(screen, font)
        
        for slider in self.sliders:
            slider.draw(screen, font)
        
        if self.compact_mode:
            stats_y = 130
            stats = [("Gen", game.generation), ("Pop", game.population), ("FPS", int(game.clock.get_fps()))]
            for i, (label, value) in enumerate(stats):
                text = f"{label}: {value}"
                surf = small_font.render(text, True, (200, 200, 200))
                screen.blit(surf, (20 + i * 80, stats_y))
        else:
            stats = [("Gen", game.generation), ("Pop", game.population), ("FPS", int(game.clock.get_fps()))]
            for i, (label, value) in enumerate(stats):
                text = f"{label}: {value}"
                surf = font.render(text, True, (220, 220, 220))
                screen.blit(surf, (25, 160 + i * 25))
            
            controls = ["SPACE-Play", "C-Clear", "R-Random", "G-Grid", "1-6-Patterns"]
            for i, text in enumerate(controls):
                surf = small_font.render(text, True, (120, 120, 120))
                screen.blit(surf, (20, 220 + i * 18))


class GameOfLife:
    def __init__(self, config, theme_manager):
        self.config = config
        self.theme_manager = theme_manager
        self.clock = None
        
        from src.game.grid import Grid
        self.grid = Grid(config.COLS, config.ROWS, config.CELL_SIZE)
        
        self.paused = True
        self.show_grid = True
        self.generation = 0
        self.population = 0
        self.target_fps = 60
        
        self.cell_colors = {}
        self.color_index = 0
        
        self.ui = AdaptiveUI()
        
        self.cell_radius = config.CELL_SIZE // 2 - 1
        self.pulse_phase = 0
        
        self.presets = {
            0: self.create_glider,
            1: self.create_blinker,
            2: self.create_beehive,
            3: self.create_lwss,
            4: self.create_pulsar,
            5: self.create_gosper,
        }

    def recreate_grid(self):
        from src.game.grid import Grid
        self.grid = Grid(self.config.COLS, self.config.ROWS, self.config.CELL_SIZE)
        self.cell_colors = {}
        self.cell_radius = max(1, self.config.CELL_SIZE // 2 - 1)

    def toggle_cell(self, row, col, set_alive=True):
        if 0 <= row < self.grid.rows and 0 <= col < self.grid.cols:
            if set_alive:
                if self.grid.cells[row, col] == 0:
                    self.grid.cells[row, col] = 1
                    self.cell_colors[(row, col)] = CellColor.get_color(self.color_index)
                    self.color_index = (self.color_index + 1) % len(CellColor.COLORS)
            else:
                self.grid.cells[row, col] = 0
                if (row, col) in self.cell_colors:
                    del self.cell_colors[(row, col)]

    def create_glider(self):
        g = np.array([[0,1,0],[0,0,1],[1,1,1]])
        self.grid.set_pattern(5, 5, g)
        self.color_index = 0
        for i in range(3):
            for j in range(3):
                if g[i, j]:
                    self.cell_colors[(5+i, 5+j)] = CellColor.get_color(self.color_index)
                    self.color_index = (self.color_index + 1) % len(CellColor.COLORS)

    def create_blinker(self):
        self.grid.set_pattern(10, 10, np.array([[1],[1],[1]]))
        self.color_index = 0
        for i in range(3):
            self.cell_colors[(10+i, 10)] = CellColor.get_color(i)

    def create_beehive(self):
        b = np.array([[0,1,1,0],[1,0,0,1],[0,1,1,0]])
        self.grid.set_pattern(15, 15, b)
        self.color_index = 0
        for i in range(3):
            for j in range(4):
                if b[i, j]:
                    self.cell_colors[(15+i, 15+j)] = CellColor.get_color(self.color_index)
                    self.color_index = (self.color_index + 1) % len(CellColor.COLORS)

    def create_lwss(self):
        l = np.array([[0,1,0,0,1],[1,0,0,0,0],[1,0,0,0,1],[1,1,1,1,0]])
        self.grid.set_pattern(20, 20, l)
        self.color_index = 0
        for i in range(4):
            for j in range(5):
                if l[i, j]:
                    self.cell_colors[(20+i, 20+j)] = CellColor.get_color(self.color_index)
                    self.color_index = (self.color_index + 1) % len(CellColor.COLORS)

    def create_pulsar(self):
        p = np.array([
            [0,0,1,1,1,0,0,0,0,1,1,1,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0],
            [1,0,0,0,0,1,0,1,0,0,0,0,1],
            [1,0,0,0,0,1,0,1,0,0,0,0,1],
            [1,0,0,0,0,1,0,1,0,0,0,0,1],
            [0,0,1,1,1,0,0,0,0,1,1,1,0],
        ])
        self.grid.set_pattern(8, 8, p)
        self.color_index = 0
        for i in range(6):
            for j in range(13):
                if p[i, j]:
                    self.cell_colors[(8+i, 8+j)] = CellColor.get_color(self.color_index)
                    self.color_index = (self.color_index + 1) % len(CellColor.COLORS)

    def create_gosper(self):
        g = np.array([
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,1,1],
            [0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,1,1,0,0,0,0,0,0,0,0,1,1],
        ])
        self.grid.set_pattern(5, 5, g)
        self.color_index = 0
        for i in range(4):
            for j in range(32):
                if j < len(g[0]) and g[i, j]:
                    self.cell_colors[(5+i, 5+j)] = CellColor.get_color(self.color_index)
                    self.color_index = (self.color_index + 1) % len(CellColor.COLORS)

    def update_cell_colors(self):
        new_colors = {}
        for row in range(self.grid.rows):
            for col in range(self.grid.cols):
                if self.grid.cells[row, col] == 1:
                    if (row, col) in self.cell_colors:
                        new_colors[(row, col)] = self.cell_colors[(row, col)]
                    else:
                        new_colors[(row, col)] = CellColor.get_color(self.color_index)
                        self.color_index = (self.color_index + 1) % len(CellColor.COLORS)
        self.cell_colors = new_colors

    def draw_cells(self, screen):
        cells = self.grid.cells
        size = self.config.CELL_SIZE
        radius = self.cell_radius
        pulse = math.sin(self.pulse_phase) * 0.1 + 0.9
        
        for row in range(self.grid.rows):
            for col in range(self.grid.cols):
                if cells[row, col] == 1:
                    cx = col * size + size // 2
                    cy = row * size + size // 2
                    
                    glow_r = int(radius * 1.5 * pulse)
                    if glow_r > 0:
                        color = self.cell_colors.get((row, col), (255, 255, 255))
                        s = pygame.Surface((glow_r * 2, glow_r * 2), pygame.SRCALPHA)
                        pygame.draw.circle(s, (*color, 30), (glow_r, glow_r), glow_r)
                        screen.blit(s, (cx - glow_r, cy - glow_r), special_flags=pygame.BLEND_ADD)
                    
                    color = self.cell_colors.get((row, col), (255, 255, 255))
                    pygame.draw.circle(screen, color, (cx, cy), radius)

    def draw_grid(self, screen):
        if self.show_grid:
            size = self.config.CELL_SIZE
            for x in range(0, self.config.WINDOW_WIDTH, size):
                pygame.draw.line(screen, (30, 30, 30), (x, 0), (x, self.config.WINDOW_HEIGHT))
            for y in range(0, self.config.WINDOW_HEIGHT, size):
                pygame.draw.line(screen, (30, 30, 30), (0, y), (self.config.WINDOW_WIDTH, y))

    def draw_hud(self, screen):
        if not self.ui.compact_mode:
            return
        panel_x = self.config.WINDOW_WIDTH - 150
        s = pygame.Surface((140, 80), pygame.SRCALPHA)
        s.fill((20, 20, 20, 200))
        screen.blit(s, (panel_x, 10))
        pygame.draw.rect(screen, (80, 80, 80), (panel_x, 10, 140, 80), 1, border_radius=8)

    def update(self):
        if not self.paused:
            self.grid.update()
            self.update_cell_colors()
            self.generation += 1
            self.population = int(np.sum(self.grid.cells))
        
        self.pulse_phase += 0.05