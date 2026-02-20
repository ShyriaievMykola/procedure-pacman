class DifficultyManager:
    def __init__(self, dif_config):
        self.DC = dif_config

    def set_easy(self):  
        self.DC.GHOST_SPEED_MS = 190
        self.DC.PACMAN_SPEED_MS = 170

    def set_medium(self):
        self.DC.GHOST_SPEED_MS = 190
        self.DC.PACMAN_SPEED_MS = 190

    def set_hard(self):
        self.DC.GHOST_SPEED_MS = 170
        self.DC.PACMAN_SPEED_MS = 190

    def set_custom(self, per_pacman, per_ghost):
        self.DC.PACMAN_SPEED_MS = per_pacman * 190 / 100
        self.DC.GHOST_SPEED_MS = per_ghost * 190 / 100

    def set_difficulty(self, level : int):
        self.DC.GHOST_SPEED_MS = 475 - 75 * level
        self.DC.PACMAN_SPEED_MS = 250 - 30 * level
        self.DC.GHOST_SPEED_MS = max(self.DC.PACMAN_SPEED_MS, self.DC.GHOST_SPEED_MS)