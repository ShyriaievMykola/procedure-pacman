import argparse

from map.map_generator import MapGenerator
from seeded_random import SeededRandom
from visualisation.visualizer import Visualizer
import random

def main():
    app_args = parse_arguments()

    print("Hello, World!")
    print()

    if app_args.test_map:
        test_map_generation()

def parse_arguments():    
    parser = argparse.ArgumentParser(description="Procedural Pac-Man Maze Generator")
    parser.add_argument('--test-map',action='store_true', help='Test map generation')
    return parser.parse_args()

def test_map_generation():
    grid_width = 21
    grid_height = 36
    seed = None

    map = MapGenerator.generate_map(grid_width, grid_height, seed)
    map.print_grid()
    print(f"Generated map with seed: {map.seed}")

    MapVisualization.display_map(map)

    srand = SeededRandom(seed=random.randint(0, 100000))
    generator = MapGenerator(grid_width, grid_height, srand=srand)
    generator.generate_map()
    generator.print_grid()
    
    # Гра в окремому вікні
    visualizer = Visualizer(generator)
    visualizer.run()
    

if __name__ == "__main__":
    main()