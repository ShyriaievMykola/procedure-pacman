from ghosts.behaviors.base_behavior import BaseBehavior

class ScatterBehavior(BaseBehavior):
    def __init__(self, color, map_width, map_height):
        """
        Логіка Scatter: рух до фіксованої точки на краях карти залежно від кольору привида.
        :param color: Колір привида.
        :param map_width: Ширина карти.
        :param map_height: Висота карти.
        """
        self.color = color
        self.map_width = map_width
        self.map_height = map_height

    def get_target(self, pacman_position):
        """
        Повертає фіксовану точку для Scatter залежно від кольору привида.
        :param ghost: Об'єкт привида (не використовується в Scatter).
        :param grid: Ігрова карта (не використовується в Scatter).
        :param pacman_position: Позиція Pacman (не використовується в Scatter).
        :return: Точка (x, y).
        """
        if self.color == "red":
            return (0, 0)  # Верхній лівий кут
        elif self.color == "blue":
            return (self.map_width - 1, 0)  # Верхній правий кут
        elif self.color == "pink":
            return (0, self.map_height - 1)  # Нижній лівий кут
        elif self.color == "orange":
            return (self.map_width - 1, self.map_height - 1)  # Нижній правий кут
        else:
            return (self.map_width // 2, self.map_height // 2)  # Центр карти за замовчуванням
