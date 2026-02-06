from ghosts.ghost import Ghost
from ghosts.behaviors.chase_behavior import ChaseBehavior
from ghosts.behaviors.scatter_behavior import ScatterBehavior
from ghosts.behaviors.frightened_behavior import FrightenedBehavior
from ghosts.behaviors.eaten_behavior import EatenBehavior
import time

class GhostManager:
    def __init__(self, map):
        self.ghosts = []
        self.grid = map.grid
        self.map_width = len(self.grid[0])
        self.map_height = len(self.grid)
        self.ghost_door = (map.ghost_door[0], map.ghost_door[1] - 1)

        # Таймери згідно з вашим зображенням (Level 1)
        # Scatter 7, Chase 20, Scatter 7, Chase 20, Scatter 5, Chase 20, Scatter 5, Chase (inf)
        self.intervals = [7, 20, 7, 20, 5, 20, 5]
        self.current_interval_index = 0
        self.last_switch_time = time.time()
        
        # Поточний режим (0, 2, 4, 6 - Scatter; 1, 3, 5, 7 - Chase)
        self.current_global_mode = "scatter" 
        self.is_frightened = False
        self.frightened_start_time = 0

        # Створення привидів
        colors = ["red", "pink", "blue", "orange"]
        for color in colors:
            self.ghosts.append(Ghost(self.ghost_door, color, self.grid))

    def update(self, pacman):
        current_time = time.time()

        # 1. ОБРОБКА ТАБЛЕТКИ (FRIGHTENED)
        if pacman.empowered and not self.is_frightened:
            self.is_frightened = True
            self.frightened_start_time = current_time # Запам'ятовуємо час початку
            for ghost in self.ghosts:
                if not isinstance(ghost.strategy, EatenBehavior):
                    ghost.change_strategy(FrightenedBehavior(ghost, self.map_width, self.map_height))
        
        elif not pacman.empowered and self.is_frightened:
            self.is_frightened = False
            # Коригуємо last_switch_time, щоб "заморозити" таймер Chase/Scatter на час переляку
            frightened_duration = current_time - self.frightened_start_time
            self.last_switch_time += frightened_duration
            
            for ghost in self.ghosts:
                if isinstance(ghost.strategy, FrightenedBehavior):
                    self._apply_global_mode(ghost)

        # 2. З'ЇДЕНІ ПРИВИДИ ТА ПОВЕРНЕННЯ ДОДОМУ
        for ghost in self.ghosts:
            # Якщо з'їли в стані переляку
            if self.is_frightened and isinstance(ghost.strategy, FrightenedBehavior):
                if ghost.position == pacman.position:
                    ghost.change_strategy(EatenBehavior(ghost, self.map_width, self.map_height, self.ghost_door))
            
            # Якщо з'їдений дійшов до бази
            if isinstance(ghost.strategy, EatenBehavior) and ghost.position == self.ghost_door:
                self._apply_global_mode(ghost)

        # 3. ТАЙМЕРИ SCATTER / CHASE (працюють тільки якщо не перелякані)
        if not self.is_frightened:
            # Перевіряємо, чи ми не дійшли до фінального нескінченного Chase (index 7)
            if self.current_interval_index < len(self.intervals):
                elapsed = current_time - self.last_switch_time
                if elapsed >= self.intervals[self.current_interval_index]:
                    self.current_interval_index += 1
                    self.last_switch_time = current_time
                    
                    # Парні індекси - Scatter, непарні - Chase
                    self.current_global_mode = "chase" if self.current_interval_index % 2 != 0 else "scatter"
                    
                    # Змінюємо стратегію всім, хто не з'їдений
                    for ghost in self.ghosts:
                        if not isinstance(ghost.strategy, EatenBehavior):
                            self._apply_global_mode(ghost)

        # 4. РУХ
        for ghost in self.ghosts:
            ghost.get_target_tile(pacman)
            ghost.move()

    def _apply_global_mode(self, ghost):
        """Допоміжний метод для призначення поточної глобальної стратегії."""
        if self.current_global_mode == "scatter":
            ghost.change_strategy(ScatterBehavior(ghost.color, self.map_width, self.map_height))
        else:
            ghost.change_strategy(ChaseBehavior(ghost, self.map_width, self.map_height))

    def be_eaten(self, ghost):
        ghost.change_strategy(EatenBehavior(ghost, self.map_width, self.map_height, self.ghost_door))

    def reset_ghosts(self):
        self.current_interval_index = 0
        self.last_switch_time = time.time()
        self.current_global_mode = "scatter"
        for ghost in self.ghosts:
            ghost.position = self.ghost_door
            self._apply_global_mode(ghost)