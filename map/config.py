class MapGeneratorConfig:
    """
    Конфіг для генератора мап
    """
    # розміри будинку привидів
    GHOST_HOUSE_WIDTH = 3
    GHOST_HOUSE_HEIGHT = 2

    # Відсоток заповнення карти монетками
    PELLET_COVERAGE = 60        # %

    # Відсоток заповнення карти підсиленнями
    POWER_COVERAGE = 0.6        # %

    DEBUG_VIEW = False
    ADVANCED_WALLS_VIEW = False