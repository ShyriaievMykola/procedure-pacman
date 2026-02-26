from typing import List, Tuple, Optional, Any
from ghosts.behaviors.base_behavior import BaseBehavior
from ghosts.behaviors.scatter_behavior import ScatterBehavior
from ghosts.utils.pathfinding import a_star
from ghosts.behaviors.frightened_behavior import FrightenedBehavior
from ghosts.behaviors.eaten_behavior import EatenBehavior

class Ghost:
    '''
    Клас, що представляє привида в грі.
    '''
    def __init__(self, position: Tuple[int, int], color: str, grid: List[List[int]], old_position: Optional[Tuple[int, int]] = None):
        """
        Ініціалізує екземпляр привида.

        Args:
            position (Tuple[int, int]): Поточні координати (x, y).
            color (str): Колір привида (визначає його Scatter-ціль).
            grid (List[List[int]]): Матриця ігрової карти.
            old_position (Optional[Tuple[int, int]]): Попередня позиція для уникнення розворотів на 180 градусів.
        """
        self.position: Tuple[int, int] = position
        self.old_position: Tuple[int, int] = old_position if old_position else position
        self.grid: List[List[int]] = grid
        self.color: str = color
        self.strategy: BaseBehavior = ScatterBehavior(color, len(grid[0]), len(grid))
        self.target_tile: Tuple[int, int] = self.position
        self.scatter_target: Tuple[int, int] = self.strategy.get_target(self, None)
        self.eaten_in_this_power_up: bool = False

    def move(self) -> Tuple[int, int]:
        """
        Обчислює шлях до цілі та оновлює позицію привида.

        Returns:
            Tuple[int, int]: Нова позиція привида після ходу.
        """
        path = a_star(self.grid, self.position, self.target_tile)
        if path:
            self.old_position = self.position
            self.position = path[0]  # Оновлюємо позицію як кортеж
        return self.position

    def change_strategy(self, new_strategy: BaseBehavior) -> None:
        """
        Змінює поточний об'єкт стратегії привида.

        Args:
            new_strategy (BaseBehavior): Нова поведінка (Chase, Scatter, Frightened або Eaten).
        """
        self.strategy = new_strategy

    def get_target_tile(self, pacman) -> Tuple[int, int]:
        """
        Запитує у поточної стратегії координати цільової клітинки.

        Args:
            pacman (Any): Об'єкт Пакмена для розрахунку траєкторії переслідування.

        Returns:
            Tuple[int, int]: Координати цільової клітинки на мапі.
        """
        if self.strategy:
            self.target_tile = self.strategy.get_target(self, pacman)
        return self.target_tile
    
    def is_frightened(self) -> bool:
        """
        Перевіряє, чи перебуває привид у стані переляку.

        Returns:
            bool: True, якщо стратегія є FrightenedBehavior.
        """
        return isinstance(self.strategy, FrightenedBehavior)

    def is_eaten(self) -> bool:
        """
        Перевіряє, чи був привид з'їдений і чи повертається він на базу.

        Returns:
            bool: True, якщо стратегія є EatenBehavior.
        """
        return isinstance(self.strategy, EatenBehavior)