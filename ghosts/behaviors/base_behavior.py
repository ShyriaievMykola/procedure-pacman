class BaseBehavior:
    def get_target(self, pacman):
        """
        Determine the target point for the ghost.
        :param pacman: The Pacman object.
        :return: Target point (x, y).
        """
        raise NotImplementedError("This method should be implemented in a subclass.")