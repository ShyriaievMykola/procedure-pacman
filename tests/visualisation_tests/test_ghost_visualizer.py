import pytest
from unittest.mock import MagicMock
from visualisation.ghost_visualizer import GhostVisualizer


@pytest.fixture
def mock_ghost_manager():
    manager = MagicMock()
    ghost1 = MagicMock()
    ghost1.position = [10.0, 10.0]
    ghost1.color = "red"
    
    ghost2 = MagicMock()
    ghost2.position = [5.0, 5.0]
    ghost2.color = "blue"
    
    manager.ghosts = [ghost1, ghost2]
    return manager


@pytest.fixture
def ghost_viz(mock_ghost_manager):
    mock_vis = MagicMock()
    return GhostVisualizer(mock_vis, mock_ghost_manager)


@pytest.mark.game_logic
def test_save_positions(ghost_viz, mock_ghost_manager):
    """Тестуємо збереження попередніх позицій привидів"""
    ghost = mock_ghost_manager.ghosts[0]
    
    ghost.position = [15.0, 12.0]
    
    ghost_viz.save_positions()
    
    assert ghost_viz.prev_pos[ghost] == [15.0, 12.0]


@pytest.mark.math_logic
def test_update_positions_interpolation(ghost_viz, mock_ghost_manager):
    """Тестуємо плавну інтерполяцію (рух) привидів"""
    ghost = mock_ghost_manager.ghosts[0]
    
    ghost_viz.prev_pos[ghost] = [10.0, 10.0]
    ghost.position = [11.0, 10.0] 
    
    ghost_viz.update_positions(0.5)
    
    assert ghost_viz.render_pos[ghost][0] == 10.5
    assert ghost_viz.render_pos[ghost][1] == 10.0


@pytest.mark.game_logic
def test_update_positions_teleportation(ghost_viz, mock_ghost_manager):
    """Тестуємо логіку телепортації (коли привид проходить через тунель)"""
    ghost = mock_ghost_manager.ghosts[0]
    
    ghost_viz.prev_pos[ghost] = [1.0, 10.0]
    ghost.position = [18.0, 10.0] 
    
    ghost_viz.update_positions(0.1)
    
    assert ghost_viz.render_pos[ghost][0] == 18.0
