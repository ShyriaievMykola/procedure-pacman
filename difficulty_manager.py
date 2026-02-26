class DifficultyManager:
    """
    Клас для управління рівнями складності гри.
    Дозволяє встановлювати швидкості руху Pac-Man та привидів для різних рівнів складності.
    """
    def __init__(self, dif_config: object) -> None:
        """
        Ініціалізація менеджера складності.
        Args:
            dif_config(object): Об'єкт конфігурації складності з параметрами швидкості
        Returns:
            None
        """
        self.DC = dif_config

    def set_easy(self) -> None:
        """
        Встановлює легкий рівень складності.
        Pac-Man рухається швидше (170 мс), привиди повільніше (190 мс).
        Args:
            None
        Returns:
            None
        """  
        self.DC.GHOST_SPEED_MS = 190
        self.DC.PACMAN_SPEED_MS = 170

    def set_medium(self) -> None:
        """
        Встановлює середній рівень складності.
        Pacman та привиди рухаються з однаковою швидкістю (190 мс).
        Args:
            None
        Returns:
            None
        """
        self.DC.GHOST_SPEED_MS = 190
        self.DC.PACMAN_SPEED_MS = 190

    def set_hard(self) -> None:
        """
        Встановлює складний рівень складності.
        Привиди рухаються швидше (170 мс), Pac-Man повільніше (190 мс).
        Args:
            None
        Returns:
            None
        """
        self.DC.GHOST_SPEED_MS = 170
        self.DC.PACMAN_SPEED_MS = 190

    def set_custom(self, per_pacman: float, per_ghost: float) -> None:
        """
        Встановлює користувацькі значення швидкості для Pac-Man та привидів.
        Значення задаються як відсотки від базової швидкості (190 мс).
        Args:
            per_pacman(float): Відсоток швидкості для Pac-Man (0-100)
            per_ghost(float): Відсоток швидкості для привидів (0-100)
        Returns:
            None
        """
        self.DC.PACMAN_SPEED_MS = per_pacman * 190 / 100
        self.DC.GHOST_SPEED_MS = per_ghost * 190 / 100

    def set_difficulty(self, level: int) -> None:
        """
        Встановлює складність за чисельним рівнем від 1 до 5.
        Де 1 - найлегше, 5 - найскладніше. Обчислює швидкість динамічно на основі рівня.
        Args:
            level(int): Рівень складності (1-5)
        Returns:
            None
        """
        self.DC.GHOST_SPEED_MS = 475 - 75 * level
        self.DC.PACMAN_SPEED_MS = 250 - 30 * level
        self.DC.GHOST_SPEED_MS = max(self.DC.PACMAN_SPEED_MS, self.DC.GHOST_SPEED_MS)