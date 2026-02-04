from ghosts.behaviors.base_behavior import BaseBehavior
import random

class FrightenedBehavior(BaseBehavior):
    def __init__(self, ghost, map_width, map_height):
        """
        Логіка Frightened: рух у випадковому напрямку, щоб уникнути Pacman.
        :param ghost: Об'єкт привида.
        :param map_width: Ширина карти.
        :param map_height: Висота карти.
        """
        self.color = ghost.color
        self.map_width = map_width
        self.map_height = map_height
        self.current_random_target = None

    def get_target(self, ghost, pacman):
        """
        Повертає випадкову точку на карті. 
        Ціль оновлюється лише тоді, коли привид її досягає.
        """
        # Якщо цілі ще немає або привид уже прийшов у призначену точку
        if self.current_random_target is None or ghost.position == self.current_random_target:
            self.current_random_target = self._generate_random_target()
        
        return self.current_random_target

    def _generate_random_target(self):
        """Генерує випадкові координати в межах сітки."""
        tx = random.randint(0, self.map_width - 1)
        ty = random.randint(0, self.map_height - 1)
        return (tx, ty)
