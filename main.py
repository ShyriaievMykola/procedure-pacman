from map_generation.map_generator import MapGenerator
from seeded_random import SeededRandom
from visualisation.visualizer import Visualizer
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
    
    # Гра в окремому вікні
    visualizer = Visualizer(generator)
    visualizer.run()
    

if __name__ == "__main__":
    main()