from ghosts.behaviors.base_behavior import BaseBehavior
from typing import Tuple, Any

class EatenBehavior(BaseBehavior):
    '''Логіка поведінки "з'їдений" для привидів'''
    def __init__(self, ghost: Any, map_width: int, map_height: int, ghost_house: Tuple[int, int]):
        """
        Логіка Eaten: привид повертається у свій будинок.
        :param ghost: Об'єкт привида.
        :param map_width: Ширина карти.
        :param map_height: Висота карти.
        """
        self.color: str = ghost.color
        self.map_width: int = map_width
        self.map_height: int = map_height
        self.ghost_house: Tuple[int, int] = ghost_house

    def get_target(self, ghost: Any, pacman: Any) -> Tuple[int, int]:
        """
        Повертає цільову точку для привида, яка є його будинком.
        """
        return self.ghost_house