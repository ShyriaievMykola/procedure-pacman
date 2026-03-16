import pytest
import time
from unittest.mock import MagicMock, patch
from ghosts.ghost_manager import GhostManager
from ghosts.behaviors.frightened_behavior import FrightenedBehavior
from ghosts.behaviors.eaten_behavior import EatenBehavior
from constants import TUNNEL


@pytest.fixture
def mock_map():
    """Створює мок об'єкта карти з необхідними атрибутами"""
    m = MagicMock()
    m.grid = [[TUNNEL] * 10 for _ in range(10)]
    m.ghost_door = (5, 5)  # Двері будинку
    return m


@pytest.fixture
def mock_pacman():
    """Створює мок Пакмена з конкретними значеннями для розрахунків"""
    p = MagicMock()
    p.position = (0, 0)
    p.movement_direction = (1, 0)
    p.empowered = False
    return p


@pytest.fixture
def manager(mock_map):
    """Ініціалізує менеджер привидів"""
    return GhostManager(mock_map)


@pytest.mark.ghost_manager
class TestGhostManager:

    def test_initialization(self, manager):
        """Перевірка початкового стану менеджера"""
        assert len(manager.ghosts) == 4  # Створюється 4 привиди
        assert manager.current_global_mode == "scatter"  # Початковий режим
        assert manager.is_frightened is False

    def test_switch_to_frightened_mode(self, manager, mock_pacman):
        """Перевірка переходу в режим переляку при підсиленні Пакмена"""
        mock_pacman.empowered = True
        manager.update(mock_pacman)
        
        assert manager.is_frightened is True
        for ghost in manager.ghosts:
            assert isinstance(ghost.strategy, FrightenedBehavior)

    @pytest.mark.powerups
    def test_return_from_frightened_mode(self, manager, mock_pacman):
        """Перевірка повернення до нормального режиму після закінчення підсилення"""
        # Спочатку входимо в режим переляку
        mock_pacman.empowered = True
        manager.update(mock_pacman)
        
        # Вимикаємо підсилення
        mock_pacman.empowered = False
        manager.update(mock_pacman)
        
        assert manager.is_frightened is False
        # Має повернутися до режиму scatter (оскільки ми ще не пройшли 5 сек)
        assert manager.current_global_mode == "scatter"

    def test_global_mode_switching_chase(self, manager, mock_pacman):
        """Перевірка перемикання зі scatter на chase за таймером"""
        # Імітуємо проходження 6 секунд (перший інтервал scatter — 5 сек)
        with patch('time.time', return_value=time.time() + 6):
            manager.update(mock_pacman)
            assert manager.current_global_mode == "chase"
            assert manager.current_interval_index == 1

    def test_be_eaten_logic(self, manager):
        """Перевірка ручного переведення привида в стан 'з'їдений'"""
        ghost = manager.ghosts[0]
        manager.be_eaten(ghost)
        assert isinstance(ghost.strategy, EatenBehavior)

    def test_ghost_returns_to_house_after_eaten(self, manager, mock_pacman):
        """Перевірка, що з'їдений привид повертається до нормальної стратегії біля дверей"""
        ghost = manager.ghosts[0]
        manager.be_eaten(ghost)
        
        # Переміщуємо привида до дверей будинку
        ghost.position = manager.ghost_door
        manager.update(mock_pacman)
        
        # Стратегія має змінитись на глобальну
        assert not isinstance(ghost.strategy, EatenBehavior)

    def test_reset_ghosts(self, manager):
        """Перевірка повного скидання стану менеджеру"""
        manager.current_global_mode = "chase"
        manager.current_interval_index = 3
        
        manager.reset_ghosts()
        
        assert manager.current_global_mode == "scatter"
        assert manager.current_interval_index == 0
        for ghost in manager.ghosts:
            assert ghost.position == manager.ghost_door
