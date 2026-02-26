import random

class SeededRandom:
    '''
    Клас для генерації випадкових чисел з фіксованим сідом.
    '''
    def __init__(self, seed: int):
        self.seed: int = seed
        self.srand: random.Random = random.Random(seed)

    def randint(self, a: int, b: int) -> int:
        """
        Генерує випадкове ціле число в межах [a, b].
        Args:
            a (int): Нижня межа.
            b (int): Верхня межа.
        Returns:
            int: Випадкове ціле число в межах [a, b].
        """
        return self.srand.randint(a, b)

    def randchance(self, chance: int) -> bool:
        """
        Генерує випадкове число та порівнює його з ймовірністю.
        Args:
            chance (int): Ймовірність (0-100).
        Returns:
            bool: True, якщо випадкове число менше за ймовірність.
        """
        return self.srand.randint(0, 100) < chance + 1

    def randfloat(self) -> float:
        """
        Генерує випадкове число з плаваючою комою в межах [0.0, 1.0).
        Returns:
            float: Випадкове число з плаваючою комою.
        """
        return self.srand.random()