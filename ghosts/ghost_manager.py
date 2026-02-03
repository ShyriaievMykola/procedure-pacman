from ghosts.ghost import Ghost

class GhostManager:
    def __init__(self, map):
        """
        Ініціалізація менеджера привидів.
        :param map: Ігрова карта (двовимірний список).
        """
        self.ghosts = []
        self.grid = map.grid

        # Визначаємо координати будиночка для привидів
        self.map_width = len(self.grid[0])
        self.map_height = len(self.grid)
        self.ghost_house_center = map.ghost_door

        # Створюємо привидів у будиночку
        self.ghosts.append(Ghost(self.ghost_house_center, "orange", self.grid))
        # self.ghosts.append(Ghost(self.ghost_house_center, "blue", grid))
        # self.ghosts.append(Ghost(self.ghost_house_center, "pink", grid))
        # self.ghosts.append(Ghost(self.ghost_house_center, "orange", grid))

    def update(self, pacman):
        for ghost in self.ghosts:
            ghost.get_target_tile(pacman.position)
            ghost.move()