from ghosts.ghost import Ghost
from ghosts.behaviors.chase_behavior import ChaseBehavior
from ghosts.behaviors.scatter_behavior import ScatterBehavior
from ghosts.behaviors.frightened_behavior import FrightenedBehavior
from ghosts.behaviors.eaten_behavior import EatenBehavior
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
        self.switch_interval = 4

        # Визначаємо координати будиночка для привидів
        self.map_width = len(self.grid[0])
        self.map_height = len(self.grid)
        self.ghost_door = (map.ghost_door[0], map.ghost_door[1] - 1)

        start_x, end_x = map.ghost_x
        start_y, end_y = map.ghost_y
        
        # Вираховуємо центральну лінію по вертикалі
        center_y = (start_y + end_y) // 2

        self.is_frightened = False

        # РОЗКОМЕНТУВАТИ КОЛИ БУДУТЬ ДВЕРІ

        # Створюємо список різних позицій для привидів всередині будиночка
        # Ми беремо точки вздовж центральної лінії будиночка
        # spawn_positions = [
        #     (start_x + 1, center_y),
        #     (end_x - 1, center_y),
        #     (start_x + 2, center_y),
        #     ((start_x + end_x) // 2, center_y) 
        # ]

        # colors = ["red", "pink", "blue", "orange"]
        # for i in range(len(colors)):
        #     pos = spawn_positions[i]
        #     color = colors[i]
        #     if color == "red":
        #         start_pos = self.ghost_door
        #     else:
        #         start_pos = pos
                
        # self.ghosts.append(Ghost(start_pos, color, self.grid))
        self.ghosts.append(Ghost(self.ghost_door, "red", self.grid))
        self.ghosts.append(Ghost(self.ghost_door, "pink", self.grid))
        self.ghosts.append(Ghost(self.ghost_door, "blue", self.grid))
        self.ghosts.append(Ghost(self.ghost_door, "orange", self.grid))

    def update(self, pacman):
        current_time = time.time()
        if pacman.empowered and not self.is_frightened:
            self.is_frightened = True
            for ghost in self.ghosts:
                if not isinstance(ghost.strategy, EatenBehavior):
                    ghost.change_strategy(FrightenedBehavior(ghost, self.map_width, self.map_height))
        elif not pacman.empowered and self.is_frightened:
            self.is_frightened = False
        
        if self.is_frightened:
            for ghost in self.ghosts:
                if isinstance(ghost.strategy, FrightenedBehavior) and ghost.position == pacman.position:
                    ghost.change_strategy(EatenBehavior(ghost, self.map_width, self.map_height, self.ghost_door))

        for ghost in self.ghosts:
            if isinstance(ghost.strategy, EatenBehavior) and ghost.position == self.ghost_door:
                ghost.change_strategy(ScatterBehavior(ghost.color, self.map_width, self.map_height))

        if not self.is_frightened:
            if current_time - self.last_switch_time >= self.switch_interval:
                for ghost in self.ghosts:
                    if isinstance(ghost.strategy, EatenBehavior):
                        continue
                    if isinstance(ghost.strategy, ScatterBehavior):
                        ghost.change_strategy(ChaseBehavior(ghost, self.map_width, self.map_height))
                    else:
                        ghost.change_strategy(ScatterBehavior(ghost.color, self.map_width, self.map_height))
                self.last_switch_time = current_time
        
        for ghost in self.ghosts:
            ghost.get_target_tile(pacman)
            ghost.move()

        def reset_ghosts(self):
            for ghost in self.ghosts:
                ghost.change_strategy(ScatterBehavior(ghost.color, self.map_width, self.map_height))
                ghost.position = self.ghost_door