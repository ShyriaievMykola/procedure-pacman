import argparse

from map.map_generator import MapGenerator
from map.map_visualization import MapVisualization
from seeded_random import SeededRandom
from visualisation.visualizer import Visualizer
from constants import *
import pacman
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

    if app_args.test_pacman:
        test_pacman()

    if app_args.test_ghost:
        test_ghost()

def parse_arguments():    
    parser = argparse.ArgumentParser(description="Procedural Pac-Man Maze Generator")
    parser.add_argument('--test-map',action='store_true', help='Test map generation')
    parser.add_argument('--test-visualization',action='store_true', help='Test map visualization')
    parser.add_argument('--test-pacman',action='store_true', help='Test pacman movement')
    parser.add_argument('--test-ghost', action='store_true', help='Test ghost behavior')
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

    srand = SeededRandom(seed=random.randint(0, 100000))
    generator = MapGenerator(grid_width, grid_height, srand=srand)
    generator.generate_map()
    generator.print_grid()


def test_pacman():
    map = get_map()
    pacman.position = pacman.get_spawn_position(map.grid)
    fps = 10
    while True:
        time.sleep(1 / fps)
        pacman.control()
        pacman.resolve_pend(map.grid)
        os.system('cls')
        map.print_grid(pacman.position)
        print(f"Points: {pacman.points}")

def test_ghost():
    map = get_map()
    # Ініціалізація Pacman
    pacman.position = pacman.get_spawn_position(map.grid)
    pacman.movement_direction = (0, 0)
    pacman.pending_direction = (0, 0)
    pacman.points = 0

    from ghosts.ghost_manager import GhostManager
    ghost_manager = GhostManager(map)
    fps = 10
    while True:
        time.sleep(1 / fps)
        pacman.control()
        pacman.resolve_pend(map.grid)
        os.system('cls')
        map.print_grid(pacman.position, ghost_manager.ghosts[0].position)
        print(f"Points: {pacman.points}, Ghost Position: {ghost_manager.ghosts[0].position}, Strategy: {type(ghost_manager.ghosts[0].strategy)}")
        ghost_manager.update(pacman)

if __name__ == "__main__":
    main()
    input()