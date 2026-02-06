from ghosts.behaviors.base_behavior import BaseBehavior
from ghosts.behaviors.scatter_behavior import ScatterBehavior
from ghosts.utils.pathfinding import a_star
from ghosts.behaviors.frightened_behavior import FrightenedBehavior
from ghosts.behaviors.eaten_behavior import EatenBehavior

class Ghost:
    def __init__(self, position, color, grid):
        self.position = position
        self.grid = grid
        self.color = color
        self.strategy = ScatterBehavior(color, len(grid[0]), len(grid))
        self.target_tile = self.position
        self.scatter_target = self.strategy.get_target(self, None)

    def move(self):
        path = a_star(self.grid, self.position, self.target_tile)
        if path:
            self.position = path[0]  # Оновлюємо позицію як кортеж
        return self.position

    def change_strategy(self, new_strategy: BaseBehavior):
        self.strategy = new_strategy

    def get_target_tile(self, pacman):
        if self.strategy:
            self.target_tile = self.strategy.get_target(self, pacman)
        return self.target_tile
    
    def is_frightened(self) -> bool:
        return isinstance(self.strategy, FrightenedBehavior)
    def is_eaten(self) -> bool:
        return isinstance(self.strategy, EatenBehavior)