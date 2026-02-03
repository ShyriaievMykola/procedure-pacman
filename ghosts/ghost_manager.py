from ghosts.ghost import Ghost
from ghosts.behaviors.chase_behavior import ChaseBehavior
from ghosts.behaviors.scatter_behavior import ScatterBehavior
from ghosts.behaviors.frightened_behavior import FrightenedBehavior
from ghosts.behaviors.eaten_behavior import EatenBehavior

class GhostManager:
    def __init__(self, ghost_positions, grid):
        """
        Initialize the GhostManager with a list of ghost positions and the game grid.
        :param ghost_positions: List of tuples [(x, y, color), ...]
        :param grid: The game grid.
        """
        self.ghosts = []
        self.grid = grid

        for pos in ghost_positions:
            x, y, color = pos
            self.ghosts.append(Ghost(x, y, color, ScatterBehavior()))  # Default state is "scatter"

    def update(self, pacman_position):
        """
        Update all ghosts' positions and states.
        :param pacman_position: The current position of Pacman (x, y).
        """
        for ghost in self.ghosts:
            if ghost.state == "scatter":
                ghost.behavior = ScatterBehavior()
            elif ghost.state == "chase":
                ghost.behavior = ChaseBehavior(pacman_position)
            elif ghost.state == "frightened":
                ghost.behavior = FrightenedBehavior()
            elif ghost.state == "eaten":
                ghost.behavior = EatenBehavior()
            ghost.move(self.grid)

    def reset(self):
        """Reset all ghosts to their initial positions."""
        for ghost in self.ghosts:
            ghost.reset(ghost.x, ghost.y)