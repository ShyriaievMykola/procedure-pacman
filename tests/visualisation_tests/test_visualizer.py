import pytest
from unittest.mock import MagicMock, patch
import pygame

from visualisation.visualizer import Visualizer

@pytest.fixture
def mock_screen():
    screen = MagicMock(spec=pygame.Surface)
    screen.get_width.return_value = 800
    screen.get_height.return_value = 600
    return screen

@pytest.fixture
def mock_map_gen():
    map_gen = MagicMock()
    map_gen.width = 20
    map_gen.height = 15
    map_gen.ghost_x = (8, 11)
    map_gen.ghost_y = (6, 8)
    return map_gen

@pytest.fixture
def visualizer(mock_screen, mock_map_gen):
    """Фікстура, що повертає готовий об'єкт візуалізатора"""
    with patch('visualisation.visualizer.CC') as mock_cc:
        mock_cc.SPEED_DIVISOR = 2
        viz = Visualizer(mock_screen, mock_map_gen)
        viz.cell = 40
        viz.x_offset = 0
        viz.y = 0
        return viz


@pytest.mark.math_logic
@pytest.mark.parametrize("grid_x, grid_y, expected_sx, expected_sy", [
    (0, 0, 0, 0),
    (5, 5, 200, 200),
    (10, 0, 400, 0),
])
def test_get_screen_pos(visualizer, grid_x, grid_y, expected_sx, expected_sy):
    """Тестуємо конвертацію координат сітки в координати екрану"""
    result = visualizer.get_screen_pos(grid_x, grid_y)
    assert result == (expected_sx, expected_sy)


@pytest.mark.game_logic
@pytest.mark.parametrize("x, y, is_inside", [
    (9, 7, True),
    (8, 6, True),
    (11, 8, True),
    (5, 5, False),
    (9, 10, False),
])
def test_is_gh(visualizer, x, y, is_inside):
    """Тестуємо логіку визначення, чи знаходиться клітинка в будинку привидів"""
    assert visualizer._is_gh(x, y) == is_inside