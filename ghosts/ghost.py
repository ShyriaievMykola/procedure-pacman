from ghosts.behaviors.base_behavior import BaseBehavior

class Ghost:
    def __init__(self, x, y, color, behavior: BaseBehavior):
        self.x = x
        self.y = y
        self.color = color
        self.behavior = behavior
        self.state = "scatter"  # States: "scatter", "chase", "frightened", "eaten"
        self.speed = 1  # Default speed
        self.target = None  # Target point for movement

    def move(self, grid):
        """Move the ghost based on its current behavior."""
        self.target = self.behavior.get_target(self)
        self.x, self.y = self.behavior.move(self, grid)

    def change_state(self, new_state):
        """Change the state of the ghost."""
        self.state = new_state
        self.behavior.on_state_change(self, new_state)

    def reset(self, start_x, start_y):
        """Reset the ghost to its initial position and state."""
        self.x = start_x
        self.y = start_y
        self.state = "scatter"  # Reset to the default state
        self.target = None