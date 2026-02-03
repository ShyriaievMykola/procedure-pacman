from ghosts.behaviors.base_behavior import BaseBehavior
from seeded_random import SeededRandom

class FrightenedBehavior(BaseBehavior):
    def __init__(self, srand: SeededRandom):
        """
        Логіка Frightened: випадковий рух.
        :param srand: Об'єкт SeededRandom для генерації випадкових чисел.
        """
        self.srand = srand

    def get_target(self, ghost):
        """
        У стані Frightened ціль не визначена, рух випадковий.
        :param ghost: Об'єкт привида.
        :return: None.
        """
        return None

    def move(self, ghost, grid):
        """
        Випадковий рух у стані Frightened.
        :param ghost: Об'єкт привида.
        :param grid: Ігрова карта.
        :return: Нова позиція (x, y).
        """
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Ліво, право, вгору, вниз
        self.srand.srand.shuffle(directions)  # Використовуємо SeededRandom для перемішування напрямків

        for dx, dy in directions:
            nx, ny = ghost.x + dx, ghost.y + dy
            if 0 <= nx < len(grid[0]) and 0 <= ny < len(grid) and grid[ny][nx] == 0:
                return nx, ny  # Повертаємо першу доступну випадкову точку

        return ghost.x, ghost.y  # Якщо немає доступних точок, залишаємося на місці