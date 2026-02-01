from map_generation.map_generator import MapGenerator
from seeded_random import SeededRandom
import random

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
    generator.print_grid()
    

if __name__ == "__main__":
    main()