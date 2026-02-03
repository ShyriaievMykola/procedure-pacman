from collections import deque
import random

from constants import *
from map.game_map import GameMap
from seeded_random import SeededRandom

class MapGenerator:        
        
    # Головний метод генерації карт
    @staticmethod
    def generate_map(width, height, seed=None):

        map = GameMap(None, height, width, None, None, None, None, None, None)

        if (seed is not None):
            map.seed = seed
            srand = SeededRandom(map.seed)
        else:
            map.seed = random.randint(0, 100000)
            srand = SeededRandom(map.seed)
        
        map.grid = [[WALL for _ in range(width)] for _ in range(height)]
        map.untouchable_zones = [[False for _ in range(width)] for _ in range(height)]

        map.ghost_x, map.ghost_y, map.ghost_door = MapGenerator.carve_ghost_room(width, height, map.grid, map.untouchable_zones)
        map.passage_left, map.passage_right = MapGenerator.carve_passages(width, height, map.grid, map.untouchable_zones)

        backup_grid = [row[:] for row in map.grid]
        backup_untouchable = [row[:] for row in map.untouchable_zones]
        correct = False

        while not correct:
            MapGenerator.grow_branches(height, width, map.grid, map.untouchable_zones, srand)
            start_x = (width // 2) - (GHOST_HOUSE_WIDTH // 2)
            start_y = (height // 2) - (GHOST_HOUSE_HEIGHT // 2)
            ghost_tunnel = (start_x - 2, start_y - 2)
            path_check_1 = MapGenerator.path_exists(map.grid, (ghost_tunnel), (width - 2, height // 2))
            path_check_2 = MapGenerator.path_exists(map.grid, (1, height // 2), (ghost_tunnel))

            print(f"Path check 1: {path_check_1}, Path check 2: {path_check_2}")
            correct = path_check_1 and path_check_2

            if not correct:
                map.grid = [row[:] for row in backup_grid]
                map.untouchable_zones = [row[:] for row in backup_untouchable]

        return map

    # Розростання гілок тунелів
    @staticmethod
    def grow_branches(height, width, grid, untouchable_zones, srand):
        tries = 3       
        iteration = 1 
        while tries > 0:
            print (f"iteration: {iteration}")
            iteration += 1
            tries -= 1
            for y in range(1, height - 1):
                for x in range(1, width - 1):
                    if grid[y][x] == WALL:
                        if srand.randchance(30):
                            carved = MapGenerator.carve_tunnel(x, y, width, height, grid, untouchable_zones)
                            if carved: tries = 3

                    elif MapGenerator.is_forming_pattern(x, y, width, height, grid) and srand.randchance(50):
                        MapGenerator.make_untouchable_zone(x, y, untouchable_zones, width, height, srand)

    @staticmethod
    def carve_tunnel(x, y, width, height, grid, untouchable_zones):
        has_tunnel = MapGenerator.has_adjacent_tunnel(x, y, grid, width, height)
        is_forming_square = MapGenerator.is_forming_square(x, y, grid)
        if (has_tunnel and not is_forming_square
            and not untouchable_zones[y][x]):
            grid[y][x] = TUNNEL
            return True
        return False

    #Позначення зони "недоторканою"
    @staticmethod
    def make_untouchable_zone(x, y, untouchable_zones, width, height, srand):
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                px = x + dx
                py = y + dy
                if 0 <= px < width and 0 <= py < height and srand.randchance(75):
                    untouchable_zones[py][px] = True

    # Вирізати будинок привидів у центрі карти
    @staticmethod
    def carve_ghost_room(width, height, grid, untouchable_zones):
        start_x = (width // 2) - (GHOST_HOUSE_WIDTH // 2)
        start_y = (height // 2) - (GHOST_HOUSE_HEIGHT // 2)
        
        # Зберегти координати будинку привидів та дверей
        ghost_x = (start_x, start_x + GHOST_HOUSE_WIDTH - 1)
        ghost_y = (start_y, start_y + GHOST_HOUSE_HEIGHT - 1)
        ghost_door = ((ghost_x[0] + ghost_x[1]) // 2, ghost_y[0] - 1)

        # Вирізати будинок привидів
        for y in range(start_y, start_y + GHOST_HOUSE_HEIGHT):
            for x in range(start_x, start_x + GHOST_HOUSE_WIDTH):
                grid[y][x] = TUNNEL


        # вирізати тунелі навколо будинку привидів
        for x in range(start_x - 2, start_x + GHOST_HOUSE_WIDTH + 2):
            grid[start_y + GHOST_HOUSE_HEIGHT + 1][x] = TUNNEL

        for x in range(start_x - 2, start_x + GHOST_HOUSE_WIDTH + 2):
            grid[start_y - 2][x] = TUNNEL

        for y in range(start_y - 2, start_y + GHOST_HOUSE_HEIGHT + 2):
            grid[y][start_x - 2] = TUNNEL
            grid[y][start_x + GHOST_HOUSE_WIDTH + 1] = TUNNEL

        # позначити зони навколо будинку привидів як недоторкані
        for y in range(start_y - 2, start_y + GHOST_HOUSE_HEIGHT + 2):
            for x in range(start_x - 2, start_x + GHOST_HOUSE_WIDTH + 2):
                untouchable_zones[y][x] = True

        return ghost_x, ghost_y, ghost_door
    
    # Вирізати тунелі з обох сторін карти
    @staticmethod
    def carve_passages(width, height, grid, untouchable_zones):
        middle_y = height // 2

        # Зберегти координати проходів
        passage_left = (0, middle_y)
        passage_right = (width - 1, middle_y)

        for x in range(3):
            grid[middle_y][x] = TUNNEL
            grid[middle_y][width - 1 - x] = TUNNEL

            for y in range(3):
                untouchable_zones[middle_y - 1 + y][x] = True
                untouchable_zones[middle_y - 1 + y][width - 1 - x] = True

        return passage_left, passage_right

    # Breadth-First Search для подальшої перевірки доступності зон
    @staticmethod
    def path_exists(grid, start, exit):
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

    # Перевірка наявності сусіднього тунелю
    @staticmethod
    def has_adjacent_tunnel(x, y, grid, width, height):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < width and 0 <= ny < height:
                if grid[ny][nx] == TUNNEL:
                    return True
        return False

    # Перевірка утворення квадрата тунелями
    @staticmethod
    def is_forming_square(x, y, grid):
        if x <= 0 or y <= 0:
            return False
        directions = [
                [(-1, 0), (0, -1), (-1, -1)],
                [(1, 0), (0, -1), (1, -1)],
                [(-1, 0), (0, 1), (-1, 1)],
                [(1, 0), (0, 1), (1, 1)]
            ]
        for direction in directions:
            if all(grid[y + dy][x + dx] == TUNNEL for dx, dy in direction):
                return True

    # Перевірка чи стіни йдуть по певному "шаблону"
    @staticmethod
    def is_forming_pattern(x, y, width, height, grid):
        patterns = [
            # Horizontal corridor
            [
                [WALL, WALL, WALL],
                [TUNNEL, TUNNEL, TUNNEL],
                [WALL, WALL, WALL],
            ],
            # Vertical corridor
            [
                [WALL, TUNNEL, WALL],
                [WALL, TUNNEL, WALL],
                [WALL, TUNNEL, WALL],
            ],
            # Top-left corner
            [
                [WALL, TUNNEL, WALL],
                [TUNNEL, TUNNEL, WALL],
                [WALL, WALL, WALL],
            ],
            # Top-right corner
            [
                [WALL, TUNNEL, WALL],
                [WALL, TUNNEL, TUNNEL],
                [WALL, WALL, WALL],
            ], 
            # Bottom-left corner
            [
                [WALL, WALL, WALL],
                [TUNNEL, TUNNEL, WALL],
                [WALL, TUNNEL, WALL],
            ],
            # Bottom-right corner
            [
                [WALL, WALL, WALL],
                [WALL, TUNNEL, TUNNEL],
                [WALL, TUNNEL, WALL],
            ],
        ]

        for pattern in patterns:
            match = True

            for dy in range(-1, 2):
                for dx in range(-1, 2):
                    px = x + dx
                    py = y + dy

                    if 0 <= px < width and 0 <= py < height:
                        cell = grid[py][px]
                    else:
                        return False

                    if cell != pattern[dy + 1][dx + 1]:
                        match = False
                        break

                if not match:
                    break

            if match:
                return True

        return False
    