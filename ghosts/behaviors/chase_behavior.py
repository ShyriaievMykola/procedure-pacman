from ghosts.behaviors.base_behavior import BaseBehavior
from typing import Tuple, Any

class ChaseBehavior(BaseBehavior):
    """
    Логіка переслідування для привидів.
    """
    def __init__(self, ghost: Any, map_width: int, map_height: int):
        """
        Логіка Chase: рух до позиції Pacman або іншої цілі залежно від кольору привида.
        :param ghost: Об'єкт привида.
        :param map_width: Ширина карти.
        :param map_height: Висота карти.
        """
        self.color: str = ghost.color
        self.map_width: int = map_width
        self.map_height: int = map_height

    def get_target(self, ghost: Any, pacman: Any) -> Tuple[int, int]:
        """
        Повертає цільову точку для Chase залежно від кольору привида.
        :param ghost: Об'єкт привида.
        :param pacman: Об'єкт Pacman.
        :return: Точка (x, y).
        """
        pacman_position = pacman.position

        if self.color == "red":
            return pacman_position

        elif self.color == "blue":
            offset = (pacman.movement_direction[0] * 4, pacman.movement_direction[1] * 4)
            return (pacman_position[0] + offset[0], pacman_position[1] + offset[1])

        elif self.color == "pink":
            offset = (-pacman.movement_direction[0] * 4, -pacman.movement_direction[1] * 4)
            return (pacman_position[0] + offset[0], pacman_position[1] + offset[1])

        elif self.color == "orange":
            distance = abs(ghost.position[0] - pacman_position[0]) + abs(ghost.position[1] - pacman_position[1])
            if distance > 8:
                return pacman_position
            else:
                return ghost.scatter_target

        else:
            return pacman_position
