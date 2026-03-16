import pytest
from unittest.mock import MagicMock, patch
from visualisation.pacman_visualizer import PacManVisualizer
import pygame

pygame.font.init()

@pytest.fixture
def mock_screen():
    screen = MagicMock()
    screen.get_width.return_value = 800
    screen.get_height.return_value = 600
    return screen

@pytest.fixture
def mock_map_gen():
    map_gen = MagicMock()
    map_gen.width = 20
    map_gen.height = 15
    map_gen.get_texture_map.return_value = []
    return map_gen

@pytest.fixture
def pacman_viz(mock_screen, mock_map_gen):
    """Фікстура для створення головного візуалізатора Pac-Man з безпечним мокуванням"""
    with patch('visualisation.pacman_visualizer.pacman') as mock_pacman, \
         patch('visualisation.pacman_visualizer.GhostManager'), \
         patch('visualisation.pacman_visualizer.state') as mock_state, \
         patch('visualisation.visualizer.CC'):
        
        mock_pacman.get_spawn_position.return_value = (10, 10)
        mock_pacman.health = 3
        mock_pacman.points = 0
        mock_pacman.empowered = False
        
        mock_state.game_instance.dif_config.PACMAN_SPEED_MS = 190
        mock_state.game_instance.dif_config.GHOST_SPEED_MS = 190
        
        viz = PacManVisualizer(mock_screen, mock_map_gen)
        viz.mock_pacman = mock_pacman
        
        yield viz

@pytest.mark.game_logic
def test_ghost_collision_loses_life(pacman_viz):
    """Тест: перевірка логіки, коли Пакман втрачає ОДНЕ життя"""
    pacman_viz.prev_health = 3
    pacman_viz.mock_pacman.health = 2
    pacman_viz.mock_pacman.empowered = False
    
    pacman_viz.check_ghost_collisions()
    
    assert pacman_viz.death_anim_playing == True
    assert pacman_viz.death_anim_game_over == False
    assert pacman_viz.reset_after_death == True

@pytest.mark.game_logic
def test_ghost_collision_game_over(pacman_viz):
    """Тест: перевірка логіки, коли Пакман втрачає ОСТАННЄ життя"""
    pacman_viz.prev_health = 1
    pacman_viz.mock_pacman.health = 0
    pacman_viz.mock_pacman.empowered = False
    
    pacman_viz.check_ghost_collisions()
    
    assert pacman_viz.death_anim_playing == True
    assert pacman_viz.death_anim_game_over == True
    assert pacman_viz.reset_after_death == False

@pytest.mark.math_logic
def test_update_camera_smoothing(pacman_viz):
    """Тест: перевірка плавного руху камери"""
    pacman_viz.screen.get_height.return_value = 600
    pacman_viz.cell = 40
    pacman_viz.max_y = 1000
    pacman_viz.render_pos = [10, 20]
    pacman_viz.y = 0
    
    with patch('visualisation.pacman_visualizer.G') as mock_g:
        mock_g.CAMERA_SMOOTHING = 0.1
        pacman_viz.update_camera()
    
    assert pacman_viz.y == 50.0