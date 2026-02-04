from ghosts.behaviors.base_behavior import BaseBehavior

class ChaseBehavior(BaseBehavior):
    def __init__(self, pacman_position):
        """
        Логіка Chase: переслідування Pacman.
        :param pacman_position: Поточна позиція Pacman (x, y).
        """
        self.pacman_position = pacman_position

    def get_target(self, ghost):
        """
        Повертає позицію Pacman як ціль.
        :param ghost: Об'єкт привида.
        :return: Точка (x, y).
        """
        return self.pacman_position

    def move(self, ghost, grid):
        """
        Рух до позиції Pacman.
        :param ghost: Об'єкт привида.
        :param grid: Ігрова карта.
        :return: Нова позиція (x, y).
        """
        from utils.pathfinding import a_star
        path = a_star(grid, (ghost.x, ghost.y), self.pacman_position)
        if path:
            return path[0]  # Повертаємо наступну точку на шляху
        return ghost.x, ghost.y  # Якщо шлях не знайдено, залишаємося на місці