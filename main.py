import argparse
from map.map_generator import MapGenerator
from map.map_visualization import MapVisualization
from game_manager import GameManager
from seeded_random import SeededRandom
from visualisation.visualizer import Visualizer
from visualisation.pacman_visualizer import PacManVisualizer
from constants import *
import pacman
import random
import os
import time
import sys
import pygame
import state

def main():
    app_args = parse_arguments()
    seed = None

    if app_args.seed is not None:
        seed = app_args.seed

    map = get_map(seed)
    print(f"using seed: {map.seed}")

    if app_args.test_texture_map:
        test_texture_map(map)

    if app_args.test_map:
        test_map_generation(map)

    if app_args.test_visualization:
        test_visualization(map)

    if app_args.test_pacman:
        test_pacman()

    if app_args.test_ghost:
        test_ghost()

    if app_args.test_menu:
        GameManager()
        state.game_instance.run()
    
    if len(sys.argv) == 1:
        GameManager()
        state.game_instance.run()

def parse_arguments():    
    parser = argparse.ArgumentParser(description="Procedural Pac-Man Maze Generator")
    parser.add_argument('--test-map',action='store_true', help='Test map generation')
    parser.add_argument('--test-visualization',action='store_true', help='Test visualization')
    parser.add_argument('--test-pacman',action='store_true', help='Test pacman movement')
    parser.add_argument('--test-ghost', action='store_true', help='Test ghost behavior')
    parser.add_argument('--test-texture-map',action='store_true', help='Test texture map')
    parser.add_argument('--test-menu',action='store_true', help='Test menu')
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
    print(game.run())

def test_pacman(map):
    pacman.position = pacman.get_spawn_position(map)
    fps = 10
    while True:
        time.sleep(1 / fps)
        pacman.old_update(map, None)
        os.system('cls')
        map.print_grid(pacman.position)
        print(f"Points: {pacman.points}")

def test_ghost():
    map = get_map()
    # Ініціалізація Pacman
    pacman.position = pacman.get_spawn_position(map)
    pacman.movement_direction = (0, 0)
    pacman.pending_direction = (0, 0)
    pacman.points = 0

    from ghosts.ghost_manager import GhostManager
    ghost_manager = GhostManager(map)
    fps = 10
    while True:
        time.sleep(1 / fps)
        pacman.old_update(map, ghost_manager)
        os.system('cls')
        map.print_grid(
            pacman.position,
            [ghost.position for ghost in ghost_manager.ghosts],
            pacman.points,
            pacman.health
        )
        print(f"Ghost Position: {ghost_manager.ghosts[0].position}, Strategy: {type(ghost_manager.ghosts[0].strategy)}")
        print(f"Is empowered: {pacman.empowered}")
        ghost_manager.update(pacman)
        
def test_texture_map(map):
    texture_map = map.get_texture_map()
    for y in range(map.height):
        row = ""
        for x in range(map.width):
            
            if (texture_map[y][x] < 10 and texture_map[y][x] != -1):
                row += f" {texture_map[y][x]} "
            else:
                row += f"{texture_map[y][x]} "

        print(row)

if __name__ == "__main__":
    try:
        main()
    except:
        import traceback
        traceback.print_exc()
        input("Press Enter to exit...")