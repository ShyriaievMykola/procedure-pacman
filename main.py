import argparse

from map.map_generator import MapGenerator
from map.map_visualization import MapVisualization
from seeded_random import SeededRandom
from visualisation.visualizer import Visualizer
from visualisation.pacman_visualizer import PacManVisualizer
from constants import *
import pacman
import random
import os
import time

def main():
    app_args = parse_arguments()

    print("Hello, World!")
    print()

    seed = None

    if app_args.seed is not None:
        seed = app_args.seed

    map = get_map(seed)
    print(f"using seed: {map.seed}")

    if app_args.test_map:
        test_map_generation(map)

    if app_args.test_visualization:
        test_visualization(map)

    if app_args.test_pacman:
        test_pacman(map)

def parse_arguments():    
    parser = argparse.ArgumentParser(description="Procedural Pac-Man Maze Generator")
    parser.add_argument('--test-map',action='store_true', help='Test map generation')
    parser.add_argument('--test-visualization',action='store_true', help='Test visualization')
    parser.add_argument('--test-pacman',action='store_true', help='Test pacman movement')
    parser.add_argument('--seed', type=int, help='Set seed')
    return parser.parse_args()

def get_map(seed=None):
    grid_width = 21
    grid_height = 36
    seed = seed

    return MapGenerator.generate_map(grid_width, grid_height, seed)


def test_map_generation(map):
    MapVisualization.display_map(map)

def test_visualization(map):
    game = PacManVisualizer(map)
    game.run()

def test_pacman(map):
    pacman.position = pacman.get_spawn_position(map.grid)
    fps = 10
    while True:
        time.sleep(1 / fps)
        pacman.control()
        pacman.resolve_pend(map.grid)
        os.system('cls')
        map.print_grid(pacman.position)
        print(f"Points: {pacman.points}")

if __name__ == "__main__":
    main()
    input()