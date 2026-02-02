from collections import deque
from constants import *

MOCK_MAP_DATA = True


class MapGenerator:

    def __init__(self, width, height, srand):
        self.width = width
        self.height = height
        self.srand = srand

        self.grid = [[WALL for _ in range(width)] for _ in range(height)]
        self.untouchable_zones = [[False for _ in range(width)] for _ in range(height)]

        self.ghost_x = None
        self.ghost_y = None
        self.ghost_door = None

        self.passage_left = None
        self.passage_right = None

    # Заглушка перед створенням генерації карти
    def generate_map(self):
        if MOCK_MAP_DATA:
            self.grid = self.mock_map_data()
            return
        
        self.carve_ghost_room()
        self.carve_passages()

    # Вирізати будинок привидів у центрі карти
    def carve_ghost_room(self):
        start_x = (self.width // 2) - (GHOST_HOUSE_WIDTH // 2)
        start_y = (self.height // 2) - (GHOST_HOUSE_HEIGHT // 2)
        
        # Зберегти координати будинку привидів та дверей
        self.ghost_x = (start_x, start_x + GHOST_HOUSE_WIDTH - 1)
        self.ghost_y = (start_y, start_y + GHOST_HOUSE_HEIGHT - 1)
        self.ghost_door = ((self.ghost_x[0] + self.ghost_x[1]) // 2, self.ghost_y[0] - 1)

        # Вирізати будинок привидів
        for y in range(start_y, start_y + GHOST_HOUSE_HEIGHT):
            for x in range(start_x, start_x + GHOST_HOUSE_WIDTH):
                self.grid[y][x] = TUNNEL

        


        # вирізати тунелі навколо будинку привидів
        for x in range(start_x - 2, start_x + GHOST_HOUSE_WIDTH + 2):
            self.grid[start_y + GHOST_HOUSE_HEIGHT + 1][x] = TUNNEL

        for x in range(start_x - 2, start_x + GHOST_HOUSE_WIDTH + 2):
            self.grid[start_y - 2][x] = TUNNEL

        for y in range(start_y - 2, start_y + GHOST_HOUSE_HEIGHT + 2):
            self.grid[y][start_x - 2] = TUNNEL
            self.grid[y][start_x + GHOST_HOUSE_WIDTH + 1] = TUNNEL

        # позначити зони навколо будинку привидів як недоторкані
        for y in range(start_y - 2, start_y + GHOST_HOUSE_HEIGHT + 2):
            for x in range(start_x - 2, start_x + GHOST_HOUSE_WIDTH + 2):
                self.untouchable_zones[y][x] = True
    
    # Вирізати тунелі з обох сторін карти
    def carve_passages(self):
        middle_y = self.height // 2

        # Зберегти координати проходів
        self.passage_left = (0, middle_y)
        self.passage_right = (self.width - 1, middle_y)

        for x in range(3):
            self.grid[middle_y][x] = TUNNEL
            self.grid[middle_y][self.width - 1 - x] = TUNNEL

            for y in range(3):
                self.untouchable_zones[middle_y - 1 + y][x] = True
                self.untouchable_zones[middle_y - 1 + y][self.width - 1 - x] = True

    # Breadth-First Search для подальшої перевірки доступності зон
    def _path_exists(self, grid, start, exit):
        h = len(grid)
        w = len(grid[0])

        sx, sy = start
        ex, ey = exit

        if grid[sy][sx] == WALL or grid[ey][ex] == WALL:
            return False

        visited = [[False]*w for _ in range(h)]
        q = deque([(sx, sy)])
        visited[sy][sx] = True

        while q:
            x, y = q.popleft()

            if (x, y) == (ex, ey):
                return True

            for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                nx, ny = x+dx, y+dy
                if 0 <= nx < w and 0 <= ny < h:
                    if not visited[ny][nx] and grid[ny][nx] == TUNNEL:
                        visited[ny][nx] = True
                        q.append((nx, ny))

        return False

    def mock_map_data(self):
        self.ghost_x = (9, 11)
        self.ghost_y = (17, 18)
        self.ghost_door = (10, 16)
        self.passage_left = (0, 18)
        self.passage_right = (20, 18)
        return [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1],
            [1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1],
            [1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1],
            [1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1],
            [1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1],
            [1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1],
            [1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1],
            [1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1],
            [1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
            [1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 0, 1],
            [1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0],
            [1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1],
            [1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1],
            [1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1],
            [1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1],
            [1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1],
            [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1],
            [1, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1],
            [1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1],
            [1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1],
            [1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1],
            [1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1],
            [1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ]
    
    # Друк карти в консоль
    def print_grid(self):
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