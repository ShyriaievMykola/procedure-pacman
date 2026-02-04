from constants import WALL

class GameMap:
    def __init__(self, seed, height, width, grid, pellet_grid, ghost_x, ghost_y, ghost_door, passage_left, passage_right):
        self.seed = seed
        self.height = height
        self.width = width
        self.grid = grid
        self.pellet_grid = pellet_grid
        self.ghost_x = ghost_x
        self.ghost_y = ghost_y
        self.ghost_door = ghost_door
        self.passage_left = passage_left
        self.passage_right = passage_right

    # Друк карти в консоль
    def print_grid(self, pacman_position=None, ghost_positions=None):
        """
        Виводить ігрову карту в консоль із візуалізацією Pacman і привидів.
        :param pacman_position: Позиція Pacman (x, y).
        :param ghost_positions: Список позицій привидів [(x1, y1), (x2, y2), ...].
        """
        for y in range(self.height):
            row = ""
            for x in range(self.width):
                if pacman_position is not None and (x, y) == pacman_position:
                    row += " ● "  # Відображення Pacman
                elif ghost_positions is not None and (x, y) in ghost_positions:
                    row += " g "  # Відображення привида
                elif (self.ghost_x[0] <= x <= self.ghost_x[1] and self.ghost_y[0] <= y <= self.ghost_y[1]):
                    row += " G "  # Відображення будиночка привидів
                elif (x, y) == self.ghost_door:
                    row += " D "  # Відображення дверей будиночка привидів
                elif (x, y) == self.passage_left:
                    row += " L "  # Відображення лівого проходу
                elif (x, y) == self.passage_right:
                    row += " R "  # Відображення правого проходу
                elif self.grid[y][x] == WALL:
                    row += "███"  # Відображення стін
                else:
                    row += "   "  # Порожній простір
            print(row)

    # отримання карти для промальовування стін
    def get_texture_map(self):

        texture_map = [[-1 for _ in range(self.width)] for _ in range(self.height)]
    
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x] == WALL:
                    mask = 0
                    
                    if y > 0 and self.grid[y-1][x] == WALL:
                        mask |= 1

                    if x < self.width - 1 and self.grid[y][x+1] == WALL:
                        mask |= 2

                    if y < self.height - 1 and self.grid[y+1][x] == WALL:
                        mask |= 4

                    if x > 0 and self.grid[y][x-1] == WALL:
                        mask |= 8
                    
                    texture_map[y][x] = mask
        return texture_map



