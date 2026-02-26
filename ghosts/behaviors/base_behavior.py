from typing import Tuple, Any
class BaseBehavior:
    def get_target(self, pacman: Any) -> Tuple[int, int]:
        """
        Отримує цільову точку для привида.

        Args:
            pacman (Any): Об'єкт Пакмена для отримання координат.

        Returns:
            Tuple[int, int]: Цільова точка (x, y) для привида.
        """
        raise NotImplementedError("This method should be implemented in a subclass.")