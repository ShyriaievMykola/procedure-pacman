from collections import deque
import math
import random

from constants import *
from map.game_map import GameMap
from seeded_random import SeededRandom
from map.config import MapGeneratorConfig as cfg

class MapGenerator:        
        
    
    @staticmethod
    def generate_map(width:int, height:int, seed:int=None) -> GameMap:
        """
        Метод для генерації карти
        Args:
            width(int): Ширина карти
            height(int): Висота карти
            seed(int): Сід для генерація карти
        Returns:
            GameMap
        """

        map = GameMap(None, height, width, None, None, None, None, None, None, None)

        if (seed is not None):
            map.seed = seed
            srand = SeededRandom(map.seed)
        else:
            map.seed = random.randint(0, 100000)
            srand = SeededRandom(map.seed)
        
        map.grid = [[WALL for _ in range(width)] for _ in range(height)]
        map.untouchable_zones = [[False for _ in range(width)] for _ in range(height)]

        map.ghost_x, map.ghost_y, map.ghost_door = MapGenerator.carve_ghost_room(map)
        map.passage_left, map.passage_right = MapGenerator.carve_passages(map)

        backup_grid = [row[:] for row in map.grid]
        backup_untouchable = [row[:] for row in map.untouchable_zones]
        correct = False

        while not correct:
            MapGenerator.grow_branches(map, srand)
            start_x = (width // 2) - (cfg.GHOST_HOUSE_WIDTH // 2)
            start_y = (height // 2) - (cfg.GHOST_HOUSE_HEIGHT // 2)
            ghost_tunnel = (start_x - 2, start_y - 2)
            path_check_1 = MapGenerator.path_exists(map.grid, (ghost_tunnel), (width - 2, height // 2))
            path_check_2 = MapGenerator.path_exists(map.grid, (1, height // 2), (ghost_tunnel))

            print(f"Path check 1: {path_check_1}, Path check 2: {path_check_2}")
            correct = path_check_1 and path_check_2

            if not correct:
                map.grid = [row[:] for row in backup_grid]
                map.untouchable_zones = [row[:] for row in backup_untouchable]
        
        MapGenerator.clear_pellet_grid(map)
        MapGenerator.spawn_pellets(map, srand)
        MapGenerator.spawn_fruit(map)
        MapGenerator.spawn_power(map)
        return map

    @staticmethod
    def clear_pellet_grid(map:GameMap):
        """
        Очищення карти підсилень
        Args:
            map(GameMap): Карта гри
        """
        map.pellet_grid = [[EMPTY for _ in range(map.width)] for _ in range(map.height)]

    @staticmethod
    def spawn_pellets(map:GameMap, srand:SeededRandom):
        """
        Генерація монеток
        Args:
            map(GameMap): Карта гри
            srand(SeededRandom): Випадкові числа за фіксованим сідом
        """
        for y in range(1, map.height - 1):
            for x in range(1, map.width - 1):
                if (map.grid[y][x] == TUNNEL):
                    if srand.randchance(cfg.PELLET_COVERAGE):
                        map.pellet_grid[y][x] = PELLET

        for y in range(map.ghost_y[0], map.ghost_y[1] + 1):
            for x in range(map.ghost_x[0], map.ghost_x[1] + 1):
                if map.pellet_grid[y][x] != EMPTY:
                    map.pellet_grid[y][x] = EMPTY

    @staticmethod
    def spawn_fruit(map:GameMap):
        """
        Спавн фрукту
        Args:
            map(GameMap): Карта гри
        """
        x = (map.ghost_x[0] + map.ghost_x[1]) // 2
        y = map.ghost_y[1] + 2
        map.pellet_grid[y][x] = FRUIT

    @staticmethod
    def spawn_power(map:GameMap):
        """
        Спавн підсилень для поїдання привидів
        Args:
            map(GameMap): Карта гри
        """
        power_count = (map.height * map.width * cfg.POWER_COVERAGE / 100) // 1

        valid_cells = [
            (x, y)
            for y in range(map.height)
            for x in range(map.width)
            if map.pellet_grid[y][x] == PELLET
        ]
        placed = [random.choice(valid_cells)]

        while len(placed) < power_count:
            best_cell = None
            best_min_dist = -1

            for cell in valid_cells:
                if cell in placed:
                    continue

                min_dist = min(MapGenerator.dist(cell, p) for p in placed)

                if min_dist > best_min_dist:
                    best_min_dist = min_dist
                    best_cell = cell

            placed.append(best_cell)

        for power in placed:
            map.pellet_grid[power[1]][power[0]] = POWER

    @staticmethod
    def dist(a:tuple[int, int], b:tuple[int, int]) -> float:
        """
        Визначення відстані по координатам
        Args:
            a (tuple[int, int]): x, y точки a
            b (tuple[int, int]): x, y точки b
        """
        return math.hypot(a[0] - b[0], a[1] - b[1])

    @staticmethod
    def grow_branches(map:GameMap, srand:SeededRandom):
        """
        Розростання гілок тунелів
        Args:
            map(GameMap): Карта гри
            srand(SeededRandom): Випадкові числа за фіксованим сідом
        """
        tries = 3       
        iteration = 1 
        while tries > 0:
            print (f"iteration: {iteration}")
            iteration += 1
            tries -= 1
            for y in range(1, map.height - 1):
                for x in range(1, map.width - 1):
                    if map.grid[y][x] == WALL:
                        if srand.randchance(30):
                            carved = MapGenerator.carve_tunnel(x, y, map)
                            if carved: tries = 3

                    elif MapGenerator.is_forming_pattern(x, y, map) and srand.randchance(50):
                        MapGenerator.make_untouchable_zone(x, y, map, srand)

    @staticmethod
    def carve_tunnel(x:int, y:int, map:GameMap):
        """
        Вибивання тунелю - перетворює стіну на тунель за відповідності умовам
        Args:
            x(int): Координата x
            y(int): Координата y
            map(GameMap): Карта гри
        """
        has_tunnel = MapGenerator.has_adjacent_tunnel(x, y, map)
        is_forming_square = MapGenerator.is_forming_square(x, y, map.grid)
        if (has_tunnel and not is_forming_square
            and not map.untouchable_zones[y][x]):
            map.grid[y][x] = TUNNEL
            return True
        return False

    @staticmethod
    def make_untouchable_zone(x:int, y:int, map:GameMap, srand:SeededRandom):
        """
        Позначення зони недоторканою за відповідності умовам
        Args:
            x(int): Координата x
            y(int): Координата y
            map(GameMap): Карта гри
            srand(SeededRandom): Випадкові числа за фіксованим сідом
        """
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                px = x + dx
                py = y + dy
                if 0 <= px < map.width and 0 <= py < map.height and srand.randchance(75):
                    map.untouchable_zones[py][px] = True

    
    @staticmethod
    def carve_ghost_room(map:GameMap) -> tuple[tuple[int, int], tuple[int, int], tuple[int, int]]:
        """
        Викарбовування кімнати з привидами
        Args:
            map(GameMap): Карта гри

        Returns:
            ghost_x, ghost_y, ghost_door
        """
        start_x = (map.width // 2) - (cfg.GHOST_HOUSE_WIDTH // 2)
        start_y = (map.height // 2) - (cfg.GHOST_HOUSE_HEIGHT // 2)
        
        # Зберегти координати будинку привидів та дверей
        ghost_x = (start_x, start_x + cfg.GHOST_HOUSE_WIDTH - 1)
        ghost_y = (start_y, start_y + cfg.GHOST_HOUSE_HEIGHT - 1)
        ghost_door = ((ghost_x[0] + ghost_x[1]) // 2, ghost_y[0] - 1)

        # Вирізати будинок привидів
        for y in range(start_y, start_y + cfg.GHOST_HOUSE_HEIGHT):
            for x in range(start_x, start_x + cfg.GHOST_HOUSE_WIDTH):
                map.grid[y][x] = TUNNEL


        # вирізати тунелі навколо будинку привидів
        for x in range(start_x - 2, start_x + cfg.GHOST_HOUSE_WIDTH + 2):
            map.grid[start_y + cfg.GHOST_HOUSE_HEIGHT + 1][x] = TUNNEL

        for x in range(start_x - 2, start_x + cfg.GHOST_HOUSE_WIDTH + 2):
            map.grid[start_y - 2][x] = TUNNEL

        for y in range(start_y - 2, start_y + cfg.GHOST_HOUSE_HEIGHT + 2):
            map.grid[y][start_x - 2] = TUNNEL
            map.grid[y][start_x + cfg.GHOST_HOUSE_WIDTH + 1] = TUNNEL

        # позначити зони навколо будинку привидів як недоторкані
        for y in range(start_y - 2, start_y + cfg.GHOST_HOUSE_HEIGHT + 2):
            for x in range(start_x - 2, start_x + cfg.GHOST_HOUSE_WIDTH + 2):
                map.untouchable_zones[y][x] = True

        return ghost_x, ghost_y, ghost_door
    
    @staticmethod
    def carve_passages(map:GameMap):
        """
        Викарбовування проходів зліва та справа карти
        Args:
            map(GameMap): Карта гри
        """
        middle_y = map.height // 2

        # Зберегти координати проходів
        passage_left = (0, middle_y)
        passage_right = (map.width - 1, middle_y)

        for x in range(3):
            map.grid[middle_y][x] = TUNNEL
            map.grid[middle_y][map.width - 1 - x] = TUNNEL

            for y in range(3):
                map.untouchable_zones[middle_y - 1 + y][x] = True
                map.untouchable_zones[middle_y - 1 + y][map.width - 1 - x] = True

        return passage_left, passage_right

    @staticmethod
    def path_exists(grid:list[list[int]], start:tuple[int,int], exit:tuple[int,int]) -> bool:
        """
        Знаходить чи є шлях між 2 точками на сітці
        Args:
            grid (list[list[int]]): сітка стін та проходів
            start (tuple[int, int]): координати точки 1
            exit (tuple[int, int]): координати точки 2 
        """
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

    @staticmethod
    def has_adjacent_tunnel(x:int, y:int, map:GameMap) -> bool:
        """
        Перевірка чи є тунелі поруч з точкою
        Args:
            x (int): координата x
            y (int): координата y
            map(GameMap): Карта гри
        """
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < map.width and 0 <= ny < map.height:
                if map.grid[ny][nx] == TUNNEL:
                    return True
        return False

    @staticmethod
    def is_forming_square(x:int, y:int, grid:list[list[int]]) -> bool:
        """
        Перевірка чи точка(стіна) є частиною квадрата
        Args:
            x (int): координата x
            y (int): координата y
            grid (list[list[int]]): сітка стін та проходів
        """
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
        return False

    @staticmethod
    def is_forming_pattern(x:int, y:int, map:GameMap) -> bool:
        """
        Перевірка чи точка(стіна) є частиною паттерну
        Args:
            x (int): координата x
            y (int): координата y
            map(GameMap): Карта гри
        """
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

                    if 0 <= px < map.width and 0 <= py < map.height:
                        cell = map.grid[py][px]
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
    