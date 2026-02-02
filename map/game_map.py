from constants import WALL

class GameMap:
    def __init__(self, height, width, grid, ghost_x, ghost_y, ghost_door, passage_left, passage_right):
        self.height = height
        self.width = width
        self.grid = grid
        self.ghost_x = ghost_x
        self.ghost_y = ghost_y
        self.ghost_door = ghost_door
        self.passage_left = passage_left
        self.passage_right = passage_right

    # Друк карти в консоль
    def print_map(self):
        for y in range(self.height):
            row = ""
            for x in range(self.width):
                if (self.ghost_x[0] <= x <= self.ghost_x[1] and self.ghost_y[0] <= y <= self.ghost_y[1]):
                    row += "G"
                elif (x, y) == self.ghost_door:
                    row += "D"
                elif (x, y) == self.passage_left:
                    row += "L"
                elif (x, y) == self.passage_right:
                    row += "R"
                elif self.grid[y][x] == WALL:
                    row += "#"
                else:
                    row += "."
            print(row)