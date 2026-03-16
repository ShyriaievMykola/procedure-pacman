import pytest
from unittest.mock import MagicMock
from ghosts.ghost import Ghost
from ghosts.behaviors.scatter_behavior import ScatterBehavior
from ghosts.behaviors.frightened_behavior import FrightenedBehavior
from constants import TUNNEL, WALL


@pytest.fixture
def simple_grid():
    """Створює просту сітку 5x5 для переміщення"""
    return [
        [TUNNEL, TUNNEL, TUNNEL, TUNNEL, TUNNEL],
        [TUNNEL, WALL,   WALL,   WALL,   TUNNEL],
        [TUNNEL, TUNNEL, TUNNEL, TUNNEL, TUNNEL],
        [TUNNEL, WALL,   WALL,   WALL,   TUNNEL],
        [TUNNEL, TUNNEL, TUNNEL, TUNNEL, TUNNEL]
    ]


@pytest.fixture
def ghost(simple_grid):
    """Створює екземпляр привида для тестів"""
    return Ghost(position=(0, 0), color="red", grid=simple_grid)


@pytest.mark.ghost_logic
class TestGhostLogic:
    
    def test_initialization(self, ghost):
        """Перевірка правильної ініціалізації об'єкта"""
        assert ghost.position == (0, 0)
        assert ghost.color == "red"
        # За замовчуванням привид має починати зі ScatterBehavior
        assert isinstance(ghost.strategy, ScatterBehavior)
        assert ghost.eaten_in_this_power_up is False

    def test_change_strategy(self, ghost):
        """Перевірка зміни об'єкта стратегії"""
        new_strategy = FrightenedBehavior(ghost, 5, 5)
        ghost.change_strategy(new_strategy)
        assert ghost.strategy == new_strategy
        assert ghost.is_frightened() is True

    def test_get_target_tile_updates_state(self, ghost):
        """Перевірка, що метод get_target_tile оновлює внутрішню ціль"""
        mock_pacman = MagicMock()
        mock_pacman.position = (2, 2)
        
        target = ghost.get_target_tile(mock_pacman)
        # Для червоного привида в Scatter ціль (0,0)
        assert ghost.target_tile == target
        assert target == (0, 0)

    @pytest.mark.pathfinding
    def test_move_updates_position(self, ghost):
        """Перевірка фізичного переміщення привида по сітці"""
        # Встановлюємо ціль праворуч від привида
        ghost.target_tile = (2, 0) 
        
        old_pos = ghost.position  # (0, 0)
        new_pos = ghost.move()
        
        # Перевіряємо, що позиція змінилася
        assert new_pos != old_pos
        assert ghost.position == new_pos
        assert ghost.old_position == old_pos
        # Згідно з A*, наступний крок від (0,0) до (2,0) має бути (1,0)
        assert new_pos == (1, 0)
