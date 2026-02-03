import argparse

from map.map_generator import MapGenerator
from map.map_visualization import MapVisualization
from seeded_random import SeededRandom
from visualisation.visualizer import Visualizer
import random
import os
import time

def main():
    app_args = parse_arguments()

    print("Hello, World!")
    print()

    if app_args.test_map:
        test_map_generation()

    if app_args.test_visualization:
        test_map_visualization()

def parse_arguments():    
    parser = argparse.ArgumentParser(description="Procedural Pac-Man Maze Generator")
    parser.add_argument('--test-map',action='store_true', help='Test map generation')
    parser.add_argument('--test-visualization',action='store_true', help='Test map visualization')
    return parser.parse_args()

def get_map():
    grid_width = 21
    grid_height = 36
    seed = None

    return MapGenerator.generate_map(grid_width, grid_height, seed)


def test_map_generation():
    map = get_map()

    MapVisualization.display_map(map)
    
    
    
# Гра в окремому вікні
def test_map_visualization():
    map = get_map()
    visualizer = Visualizer(map)
    visualizer.run()

if __name__ == "__main__":
    main()
    input()