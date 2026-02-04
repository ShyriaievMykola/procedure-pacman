class BaseBehavior:
    def get_target(self, pacman_position):
        """
        Determine the target point for the ghost.
        :param pacman_position: The position of Pacman.
        :return: Target point (x, y).
        """
        raise NotImplementedError("This method should be implemented in a subclass.")