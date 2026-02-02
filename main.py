from map_generation.map_generator import MapGenerator
from seeded_random import SeededRandom
from constants import *
import pacman
import random
import os
import time

def main():
    print("Hello, World!")
    print()

    # Не змінювати до повноцінної імплементації генератора карти
    tile_size = 20
    grid_width = 21
    grid_height = 36

    srand = SeededRandom(seed=random.randint(0, 100000))
    generator = MapGenerator(grid_width, grid_height, srand=srand)
    generator.generate_map()
    generator.fill_with_pellets()
    pacman.position = pacman.get_spawn_position(generator.grid)
    fps = 10
    while True:
        time.sleep(1 / fps)
        generator.grid[pacman.position[1]][pacman.position[0]] = EMPTY
        pacman.control()
        pacman.resolve_pend(generator.grid)
        generator.grid[pacman.position[1]][pacman.position[0]] = PACMAN
        os.system('cls')
        generator.print_grid()
        print(f"Points: {pacman.points}")

if __name__ == "__main__":
    main()
    input()