from ghosts.behaviors.base_behavior import BaseBehavior

class EatenBehavior(BaseBehavior):
    def __init__(self, ghost, map_width, map_height, ghost_house):
        """
        Логіка Eaten: привид повертається у свій будинок.
        :param ghost: Об'єкт привида.
        :param map_width: Ширина карти.
        :param map_height: Висота карти.
        """
        self.color = ghost.color
        self.map_width = map_width
        self.map_height = map_height
        self.ghost_house = ghost_house

    def get_target(self, ghost, pacman):
        """
        Повертає цільову точку для привида, яка є його будинком.
        """
        return self.ghost_house