"""
Conway's Game of Life - Main Runner
Simple entry point that launches the game.
"""

import pygame
import sys

try:
    from src.utils.config import Config
    from src.game.game_logic import GameOfLife, AdaptiveUI
except ImportError:
    from utils.config import Config
    from game.game_logic import GameOfLife, AdaptiveUI


def main():
    pygame.init()
    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
    
    config = Config()
    
    screen = pygame.display.set_mode(
        (config.WINDOW_WIDTH, config.WINDOW_HEIGHT),
        pygame.RESIZABLE | pygame.DOUBLEBUF
    )
    pygame.display.set_caption("Conway's Game of Life")
    
    clock = pygame.time.Clock()
    game = GameOfLife(config, None)
    game.ui.create_elements(config.WINDOW_WIDTH, config.WINDOW_HEIGHT)
    game.clock = clock
    
    _setup_buttons(game)
    
    font = pygame.font.Font(None, 24)
    small_font = pygame.font.Font(None, 16)
    
    running = True
    
    while running:
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.KEYDOWN:
                handle_keypress(game, event.key)
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                handle_click(game, event)
            
            elif event.type == pygame.VIDEORESIZE:
                config.WINDOW_WIDTH = event.w
                config.WINDOW_HEIGHT = event.h
                game.recreate_grid()
                game.ui.create_elements(event.w, event.h)
                _setup_buttons(game)
                pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE | pygame.DOUBLEBUF)
        
        for button in game.ui.buttons:
            button.update(mouse_pos, mouse_pressed)
        
        for slider in game.ui.sliders:
            slider.update(mouse_pos, mouse_pressed)
            if slider.label == "Speed":
                config.FPS = int(slider.value)
                game.target_fps = int(slider.value)
            elif slider.label == "Colors":
                from src.game.game_logic import CellColor
                CellColor.set_max_colors(int(slider.value))
        
        game.update()
        
        screen.fill((5, 5, 5))
        
        game.draw_grid(screen)
        game.draw_cells(screen)
        
        game.ui.draw(screen, game, font, small_font)
        game.draw_hud(screen)
        
        pygame.display.flip()
        clock.tick(config.FPS)
    
    pygame.quit()
    sys.exit()


def _setup_buttons(game):
    for btn in game.ui.buttons:
        if btn.text == "Play":
            btn.callback = lambda: setattr(game, 'paused', False)
        elif btn.text == "Clear":
            btn.callback = lambda: (game.grid.clear(), setattr(game, 'generation', 0), setattr(game, 'population', 0))
        elif btn.text == "Random":
            btn.callback = lambda: (game.grid.randomize(), setattr(game, 'generation', 0))
        elif btn.text == "Grid":
            btn.callback = lambda: setattr(game, 'show_grid', not game.show_grid)
        elif btn.text == "Slow":
            btn.callback = lambda: setattr(game, 'target_fps', max(1, game.target_fps - 10))
        elif btn.text == "Fast":
            btn.callback = lambda: setattr(game, 'target_fps', min(120, game.target_fps + 10))


def handle_keypress(game, key):
    if key == pygame.K_SPACE:
        game.paused = not game.paused
    elif key == pygame.K_c:
        game.grid.clear()
        game.generation = 0
        game.population = 0
    elif key == pygame.K_r:
        game.grid.randomize()
        game.generation = 0
    elif key == pygame.K_g:
        game.show_grid = not game.show_grid
    elif key == pygame.K_ESCAPE:
        sys.exit()
    elif key == pygame.K_UP:
        game.target_fps = min(120, game.target_fps + 10)
        _update_slider(game, "Speed", game.target_fps)
    elif key == pygame.K_DOWN:
        game.target_fps = max(1, game.target_fps - 10)
        _update_slider(game, "Speed", game.target_fps)
    elif pygame.K_1 <= key <= pygame.K_6:
        idx = key - pygame.K_1
        if idx in game.presets:
            game.grid.clear()
            game.presets[idx]()
            game.generation = 0


def handle_click(game, event):
    if event.button == 1:
        col = event.pos[0] // game.config.CELL_SIZE
        row = event.pos[1] // game.config.CELL_SIZE
        
        if 0 <= row < game.grid.rows and 0 <= col < game.grid.cols:
            if game.grid.cells[row, col] == 0:
                game.toggle_cell(row, col, True)
            else:
                game.toggle_cell(row, col, False)


def _update_slider(game, label, value):
    for s in game.ui.sliders:
        if s.label == label:
            s.value = value
            break


if __name__ == "__main__":
    main()