from ghosts.ghost import Ghost
from ghosts.behaviors.chase_behavior import ChaseBehavior
from ghosts.behaviors.scatter_behavior import ScatterBehavior
import time

class GhostManager:
    def __init__(self, map):
        """
        Ініціалізація менеджера привидів.
        :param map: Ігрова карта (двовимірний список).
        """
        self.ghosts = []
        self.grid = map.grid
        self.last_switch_time = time.time()
        self.switch_interval = 5

        # Визначаємо координати будиночка для привидів
        self.map_width = len(self.grid[0])
        self.map_height = len(self.grid)
        self.ghost_house_center = map.ghost_door

        # Створюємо привидів у будиночку
        self.ghosts.append(Ghost(self.ghost_house_center, "orange", self.grid))
        self.ghosts.append(Ghost(self.ghost_house_center, "blue", self.grid))
        self.ghosts.append(Ghost(self.ghost_house_center, "pink", self.grid))
        self.ghosts.append(Ghost(self.ghost_house_center, "red", self.grid))

    def update(self, pacman):
        current_time = time.time()
        
        if current_time - self.last_switch_time >= self.switch_interval:
            for ghost in self.ghosts:
                if isinstance(ghost.strategy, ScatterBehavior):
                    ghost.change_strategy(ChaseBehavior(ghost, self.map_width, self.map_height))
                else:
                    ghost.change_strategy(ScatterBehavior(ghost.color, self.map_width, self.map_height))
            self.last_switch_time = current_time

        for ghost in self.ghosts:
            ghost.get_target_tile(pacman)
            ghost.move()