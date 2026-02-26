from ghosts.ghost import Ghost
from ghosts.behaviors.chase_behavior import ChaseBehavior
from ghosts.behaviors.scatter_behavior import ScatterBehavior
from ghosts.behaviors.frightened_behavior import FrightenedBehavior
from ghosts.behaviors.eaten_behavior import EatenBehavior
import time
from typing import List, Tuple, Any

class GhostManager:
    """
    Контролер, що керує станом та поведінкою всіх привидів у грі.
    
    Відповідає за глобальні таймери (Chase/Scatter), обробку станів переляку 
    після з'їдання таблетки та координацію взаємодії привидів з Пакменом.
    """
    def __init__(self, map: Any):
        """
        Ініціалізує менеджер привидів та створює початковий набір привидів.

        Args:
            game_map (Any): Об'єкт мапи, що містить сітку (grid) та координати дверей (ghost_door).
        """
        self.ghosts: List[Ghost] = []
        self.grid: List[List[int]] = map.grid
        self.map_width: int = len(self.grid[0])
        self.map_height: int = len(self.grid)
        self.ghost_door: Tuple[int, int] = (map.ghost_door[0], map.ghost_door[1] - 1)
        self.intervals: List[int] = [5, 20, 5, 20, 4, 20, 4]
        self.current_interval_index: int = 0
        self.last_switch_time: float = time.time()
        self.current_global_mode: str = "scatter"
        self.is_frightened: bool = False
        self.frightened_start_time: float = 0
        colors: List[str] = ["red", "pink", "blue", "orange"]
        for color in colors:
            self.ghosts.append(Ghost(self.ghost_door, color, self.grid))

    def update(self, pacman: Any) -> None:
        """
        Оновлює стан усіх привидів залежно від часу та дій Пакмена.

        Метод обробляє:
        1. Перехід у режим переляку (Frightened).
        2. Повернення до нормального режиму після завершення дії таблетки.
        3. З'їдання привидів Пакменом.
        4. Глобальні таймери зміни фаз Chase/Scatter.

        Args:
            pacman (Any): Об'єкт гравця для перевірки колізій та отримання координат.
        """
        current_time = time.time()

        if pacman.empowered and not self.is_frightened:
            self.is_frightened = True
            self.frightened_start_time = current_time
            for ghost in self.ghosts:
                if not isinstance(ghost.strategy, EatenBehavior):
                    ghost.change_strategy(FrightenedBehavior(ghost, self.map_width, self.map_height))
        
        elif not pacman.empowered and self.is_frightened:
            self.is_frightened = False
            frightened_duration = current_time - self.frightened_start_time
            self.last_switch_time += frightened_duration
            
            for ghost in self.ghosts:
                if isinstance(ghost.strategy, FrightenedBehavior):
                    self._apply_global_mode(ghost)

        for ghost in self.ghosts:
            if self.is_frightened and isinstance(ghost.strategy, FrightenedBehavior):
                if ghost.position == pacman.position:
                    ghost.change_strategy(EatenBehavior(ghost, self.map_width, self.map_height, self.ghost_door))
            if isinstance(ghost.strategy, EatenBehavior) and ghost.position == self.ghost_door:
                ghost.eaten_in_this_power_up = False
                self._apply_global_mode(ghost)

        if not self.is_frightened:
            if self.current_interval_index < len(self.intervals):
                elapsed = current_time - self.last_switch_time
                if elapsed >= self.intervals[self.current_interval_index]:
                    self.current_interval_index += 1
                    self.last_switch_time = current_time
                    self.current_global_mode = "chase" if self.current_interval_index % 2 != 0 else "scatter"
                    for ghost in self.ghosts:
                        if not isinstance(ghost.strategy, EatenBehavior):
                            self._apply_global_mode(ghost)
        for ghost in self.ghosts:
            ghost.get_target_tile(pacman)
            ghost.move()

    def _apply_global_mode(self, ghost: Ghost) -> None:
        """
        Призначає привиду стратегію згідно з поточним глобальним режимом гри.

        Args:
            ghost (Ghost): Об'єкт привида, якому потрібно змінити стратегію.
        """
        if self.current_global_mode == "scatter":
            ghost.change_strategy(ScatterBehavior(ghost.color, self.map_width, self.map_height))
        else:
            ghost.change_strategy(ChaseBehavior(ghost, self.map_width, self.map_height))

    def be_eaten(self, ghost: Ghost) -> None:
        """
        Переводить привида у стан "з'їдений" (повернення до бази).

        Args:
            ghost (Ghost): Привид, якого з'їв Пакмен.
        """
        ghost.change_strategy(EatenBehavior(ghost, self.map_width, self.map_height, self.ghost_door))

    def reset_ghosts(self) -> None:
        """
        Скидає стан усіх привидів до початкового (наприклад, після втрати життя).
        """
        self.current_interval_index = 0
        self.last_switch_time = time.time()
        self.current_global_mode = "scatter"
        for ghost in self.ghosts:
            ghost.position = self.ghost_door
            ghost.eaten_in_this_power_up = False
            self._apply_global_mode(ghost)