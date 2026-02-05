from ghosts.behaviors.base_behavior import BaseBehavior

class ChaseBehavior(BaseBehavior):
    def __init__(self, ghost, map_width, map_height):
        """
        Логіка Chase: рух до позиції Pacman або іншої цілі залежно від кольору привида.
        :param ghost: Об'єкт привида.
        :param map_width: Ширина карти.
        :param map_height: Висота карти.
        """
        self.color = ghost.color
        self.map_width = map_width
        self.map_height = map_height

    def get_target(self, ghost, pacman):
        """
        Повертає цільову точку для Chase залежно від кольору привида.
        :param ghost: Об'єкт привида.
        :param pacman: Об'єкт Pacman.
        :return: Точка (x, y).
        """
        pacman_position = pacman.position

        if self.color == "red":
            # Червоний привид переслідує поточну позицію Pacman
            return pacman_position

        elif self.color == "blue":
            # Синій привид переслідує точку на кілька клітинок попереду Pacman
            offset = (pacman.movement_direction[0] * 4, pacman.movement_direction[1] * 4)
            return (pacman_position[0] + offset[0], pacman_position[1] + offset[1])

        elif self.color == "pink":
            # Рожевий привид переслідує точку на кілька клітинок позаду Pacman
            offset = (-pacman.movement_direction[0] * 4, -pacman.movement_direction[1] * 4)
            return (pacman_position[0] + offset[0], pacman_position[1] + offset[1])

        elif self.color == "orange":
            # Помаранчевий привид переслідує Pacman, але якщо близько, повертається до Scatter
            distance = abs(ghost.position[0] - pacman_position[0]) + abs(ghost.position[1] - pacman_position[1])
            if distance > 8:  # Якщо далеко, переслідує Pacman
                return pacman_position
            else:  # Якщо близько, повертається до своєї точки Scatter
                return ghost.scatter_target

        else:
            # За замовчуванням переслідує поточну позицію Pacman
            return pacman_position
