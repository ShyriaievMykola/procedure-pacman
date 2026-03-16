import pytest
from unittest.mock import MagicMock
from ghosts.behaviors.scatter_behavior import ScatterBehavior
from ghosts.behaviors.chase_behavior import ChaseBehavior
from ghosts.behaviors.frightened_behavior import FrightenedBehavior
from ghosts.behaviors.eaten_behavior import EatenBehavior

# Допоміжні об'єкти для тестів
@pytest.fixture
def mock_pacman():
    pacman = MagicMock()
    pacman.position = (10, 10)
    pacman.movement_direction = (1, 0) # Рух вправо
    return pacman

@pytest.fixture
def mock_ghost():
    ghost = MagicMock()
    ghost.color = "red"
    ghost.position = (5, 5)
    ghost.scatter_target = (0, 0)
    return ghost

class TestScatterBehavior:
    """Тести для ScatterBehavior"""
    
    def test_red_target(self, mock_pacman):
        strategy = ScatterBehavior("red", 20, 20)
        assert strategy.get_target(None, mock_pacman) == (0, 0)

    def test_pink_target(self, mock_pacman):
        strategy = ScatterBehavior("pink", 20, 20)
        assert strategy.get_target(None, mock_pacman) == (0, 19)

    def test_blue_target(self, mock_pacman):
        strategy = ScatterBehavior("blue", 20, 20)
        assert strategy.get_target(None, mock_pacman) == (19, 0)

    def test_orange_target(self, mock_pacman):
        strategy = ScatterBehavior("orange", 20, 20)
        assert strategy.get_target(None, mock_pacman) == (19, 19)

class TestChaseBehavior:
    """Тести для ChaseBehavior"""

    def test_red_chase_target(self, mock_ghost, mock_pacman):
        mock_ghost.color = "red"
        strategy = ChaseBehavior(mock_ghost, 20, 20)
        assert strategy.get_target(mock_ghost, mock_pacman) == (10, 10)

    def test_pink_chase_target(self, mock_ghost, mock_pacman):
        mock_ghost.color = "pink"
        mock_pacman.movement_direction = (1, 0) # Вправо
        strategy = ChaseBehavior(mock_ghost, 20, 20)
        # Pink цілиться на 4 клітинки попереду
        # (10 + (-1*4), 10 + (0*4)) = (6, 10)
        assert strategy.get_target(mock_ghost, mock_pacman) == (6, 10)

    def test_orange_chase_far(self, mock_ghost, mock_pacman):
        mock_ghost.color = "orange"
        mock_ghost.position = (0, 0) # Далеко від Пакмена (відстань > 8)
        mock_ghost.scatter_target = (19, 19)
        strategy = ChaseBehavior(mock_ghost, 20, 20)
        # Якщо далеко, цілиться в Пакмена
        assert strategy.get_target(mock_ghost, mock_pacman) == (10, 10)

    def test_orange_chase_near(self, mock_ghost, mock_pacman):
        mock_ghost.color = "orange"
        mock_ghost.position = (9, 9) # Близько до Пакмена (відстань <= 8)
        mock_ghost.scatter_target = (19, 19)
        strategy = ChaseBehavior(mock_ghost, 20, 20)
        # Якщо близько, цілиться в свій scatter кут
        assert strategy.get_target(mock_ghost, mock_pacman) == (19, 19)

class TestFrightenedBehavior:
    """Тести для FrightenedBehavior"""

    def test_generates_random_target(self, mock_ghost, mock_pacman):
        strategy = FrightenedBehavior(mock_ghost, 20, 20)
        target = strategy.get_target(mock_ghost, mock_pacman)
        # Перевірка меж
        assert 0 <= target[0] < 20
        assert 0 <= target[1] < 20

    def test_persists_target_until_reached(self, mock_ghost, mock_pacman):
        strategy = FrightenedBehavior(mock_ghost, 20, 20)
        target1 = strategy.get_target(mock_ghost, mock_pacman)
        
        # Позиція привида ще не збігається з ціллю
        mock_ghost.position = (-1, -1) 
        target2 = strategy.get_target(mock_ghost, mock_pacman)
        
        # Ціль не повинна змінитись
        assert target1 == target2

class TestEatenBehavior:
    """Тести для EatenBehavior"""

    def test_returns_to_ghost_house(self, mock_ghost, mock_pacman):
        house = (10, 8)
        strategy = EatenBehavior(mock_ghost, 20, 20, house)
        # Завжди повертає координати будинку
        assert strategy.get_target(mock_ghost, mock_pacman) == house