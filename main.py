import argparse
from typing import Optional, Tuple, Any
from map.map_generator import MapGenerator
from map.map_visualization import MapVisualization
from game_manager import GameManager
from seeded_random import SeededRandom
from visualisation.visualizer import Visualizer
from visualisation.pacman_visualizer import PacManVisualizer
from constants import *
import sys
import pygame
import state

def main() -> None:
    """
    Головна функція входу в програму.
    
    Визначає режим запуску:
    - Якщо передані аргументи командного рядка: запускає тестові візуалізації мапи.
    - Якщо аргументів немає: запускає основний ігровий цикл через GameManager.
    """
    app_args = parse_arguments()
    if len(sys.argv) > 1:
        pygame.init()
        seed = None
        if app_args.seed is not None:
            seed = app_args.seed

        map = get_map(seed)
        print(f"using seed: {map.seed}")

        if app_args.test_texture_map:
            test_texture_map(map)

        if app_args.test_map:
            offset = (0, 0)
            size = (map.width * 20, map.height * 20)
            screen = pygame.display.set_mode(size)
            pygame.display.set_caption(f"Map Test - Seed: {map.seed}")
            test_map_generation(screen, size, offset, map)

    else:
        GameManager()
        state.game_instance.run()

def parse_arguments() -> argparse.Namespace:
    """
    Парсить аргументи командного рядка для налаштування запуску.

    Returns:
        argparse.Namespace: Об'єкт із розпарсеними прапорцями (--test-map, --seed тощо).
    """    
    parser = argparse.ArgumentParser(description="Procedural Pac-Man Maze Generator")
    parser.add_argument('--test-map',action='store_true', help='Test map generation')
    parser.add_argument('--test-texture-map',action='store_true', help='Test texture map')
    parser.add_argument('--seed', type=int, help='Set seed')
    return parser.parse_args()

def get_map(seed: int | None = None) -> Any:
    """
    Ініціалізує генератор мапи з заданими параметрами.

    Args:
        seed (Optional[int]): Сід для генерації. Якщо None, буде використано випадковий.

    Returns:
        Any: Об'єкт згенерованої мапи (Map object).
    """
    grid_width = 21
    grid_height = 36
    seed = seed

    return MapGenerator.generate_map(grid_width, grid_height, seed)

def test_map_generation(screen: pygame.Surface, size: Tuple[int, int], offset: Tuple[int, int], map: Any) -> None:
    """
    Запускає окремий цикл Pygame для візуальної перевірки згенерованої мапи.

    Args:
        screen (pygame.Surface): Поверхня для малювання.
        size (Tuple[int, int]): Розмір вікна.
        offset (Tuple[int, int]): Зміщення малювання.
        map_obj (Any): Об'єкт мапи, який треба відобразити.
    """
    running = True
    clock = pygame.time.Clock()
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((0, 0, 0))
        MapVisualization.display_map(screen, size, offset, map)
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

def test_texture_map(map: Any) -> None:
    """
    Виводить текстове представлення текстурної мапи в консоль.
    Використовується для налагодження індексів стін та проходів.

    Args:
        map_obj (Any): Об'єкт мапи для аналізу.
    """
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
    main()
    exit(0)