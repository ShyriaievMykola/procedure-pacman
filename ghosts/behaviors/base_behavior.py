class BaseBehavior:
    def get_target(self, ghost):
        """
        Determine the target point for the ghost.
        :param ghost: The ghost object.
        :return: Target point (x, y).
        """
        raise NotImplementedError("This method should be implemented in a subclass.")

    def move(self, ghost, grid):
        """
        Move the ghost based on its behavior.
        :param ghost: The ghost object.
        :param grid: The game grid.
        :return: New position (x, y).
        """
        raise NotImplementedError("This method should be implemented in a subclass.")

    def on_state_change(self, ghost, new_state):
        """
        Handle state changes for the ghost.
        :param ghost: The ghost object.
        :param new_state: The new state of the ghost.
        """
        pass