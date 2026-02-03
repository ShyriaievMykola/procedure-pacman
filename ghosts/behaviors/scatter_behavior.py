from ghosts.behaviors.base_behavior import BaseBehavior

class ScatterBehavior(BaseBehavior):
    def __init__(self, scatter_target):
        """
        Логіка Scatter: рух до фіксованої точки на карті.
        :param scatter_target: Фіксована точка (x, y), до якої рухається привид.
        """
        self.scatter_target = scatter_target

    def get_target(self, ghost):
        """
        Повертає фіксовану точку для Scatter.
        :param ghost: Об'єкт привида.
        :return: Точка (x, y).
        """
        return self.scatter_target

    def move(self, ghost, grid):
        """
        Рух до фіксованої точки.
        :param ghost: Об'єкт привида.
        :param grid: Ігрова карта.
        :return: Нова позиція (x, y).
        """
        from utils.pathfinding import a_star
        path = a_star(grid, (ghost.x, ghost.y), self.scatter_target)
        if path:
            return path[0]  # Повертаємо наступну точку на шляху
        return ghost.x, ghost.y  # Якщо шлях не знайдено, залишаємося на місці