from constants import WALL, PELLET, POWER, FRUIT

class GameMap:
    """
    Клас карти, включає всі дані про згенеровану карту.
    Attributes:
        seed (int): Сід карти
        height (int): Висота карти
        width (int): Ширина карти
        grid (list[list[int]]): Сітка карти
        pellet_grid (list[list[int]]): Сітка підсилень
        ghost_x (tuple[int, int]): Початок та кінець координат кімнати привидів по осі Х
        ghost_y (tuple[int, int]): Початок та кінець координат кімнати привидів по осі У
        ghost_door (tuple[int, int]): Координати (x,y) дверей кімнати привидів
        passage_left (tuple[int, int]): Координати (x,y) лівого проходу
        passage_right (tuple[int, int]): Координати (x,y) правого проходу
    """
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

    
    def print_grid(self, pacman_position:tuple[int, int]=None, ghost_positions=None, points:int=0, health:int=3):
        """
        Друк карти у консольному вигляді
        Args:
            pacman_position(tuple[int, int]): Позиція пекмена (x,y)
            ghost_positions(list[tuple[int, int]]): Позиції привидів (x,y)
            points(int): Очки гри
            health(int): Життя пекмена
        """
        for y in range(self.height):
            row = ""
            for x in range(self.width):
                if pacman_position is not None and (x, y) == pacman_position:
                    row += " ● "
                elif ghost_positions is not None and (x, y) in ghost_positions:
                    row += " g "
                elif (self.ghost_x[0] <= x <= self.ghost_x[1] and self.ghost_y[0] <= y <= self.ghost_y[1]):
                    row += " G "
                elif (x, y) == self.ghost_door:
                    row += " D "
                elif self.grid[y][x] == WALL:
                    row += "███"
                else:
                    pellet = self.pellet_grid[y][x]
                    if pellet == PELLET: row += " . "
                    elif pellet == POWER: row += " o "
                    elif pellet == FRUIT: row += " f "
                    else: row += "   "
            print(row)
        print(f"\nSCORE: {points} | LIVES: {health}")

   
    def get_texture_map(self):
        """
        Отримання мапи текстур для покращеного промальвування стін
        """
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



