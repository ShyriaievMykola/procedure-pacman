from ghosts.behaviors.base_behavior import BaseBehavior
import random
from typing import Tuple, Any

class FrightenedBehavior(BaseBehavior):
    def __init__(self, ghost: Any, map_width: int, map_height: int):
        """
        Логіка Frightened: рух у випадковому напрямку, щоб уникнути Pacman.
        :param ghost: Об'єкт привида.
        :param map_width: Ширина карти.
        :param map_height: Висота карти.
        """
        self.color: str = ghost.color
        self.map_width: int = map_width
        self.map_height: int = map_height
        self.current_random_target: Tuple[int, int] = None

    def get_target(self, ghost: Any, pacman: Any) -> Tuple[int, int]:
        """
        Повертає випадкову точку на карті. 
        Ціль оновлюється лише тоді, коли привид її досягає.
        """
        if self.current_random_target is None or ghost.position == self.current_random_target:
            self.current_random_target = self._generate_random_target()
        
        return self.current_random_target

    def _generate_random_target(self) -> Tuple[int, int]:
        """Генерує випадкові координати в межах сітки."""
        tx = random.randint(0, self.map_width - 1)
        ty = random.randint(0, self.map_height - 1)
        return (tx, ty)
