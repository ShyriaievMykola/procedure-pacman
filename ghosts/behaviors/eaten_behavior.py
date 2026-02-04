from ghosts.behaviors.base_behavior import BaseBehavior
from utils.pathfinding import a_star

class EatenBehavior(BaseBehavior):
    def __init__(self, ghost_house_position):
        """
        Логіка Eaten: повернення до будинку привидів.
        :param ghost_house_position: Позиція будинку привидів (x, y).
        """
        self.ghost_house_position = ghost_house_position

    def get_target(self, ghost):
        """
        Повертає позицію будинку привидів як ціль.
        :param ghost: Об'єкт привида.
        :return: Точка (x, y).
        """
        return self.ghost_house_position

    def move(self, ghost, grid):
        """
        Рух до будинку привидів.
        :param ghost: Об'єкт привида.
        :param grid: Ігрова карта.
        :return: Нова позиція (x, y).
        """
        path = a_star(grid, (ghost.x, ghost.y), self.ghost_house_position)
        if path:
            return path[0]  # Повертаємо наступну точку на шляху
        return ghost.x, ghost.y  # Якщо шлях не знайдено, залишаємося на місці

    def on_state_change(self, ghost, new_state):
        """
        Якщо привид досягає будинку, змінюємо стан на Scatter.
        :param ghost: Об'єкт привида.
        :param new_state: Новий стан.
        """
        if (ghost.x, ghost.y) == self.ghost_house_position:
            ghost.change_state("scatter")