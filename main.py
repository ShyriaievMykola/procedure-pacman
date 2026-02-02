from map.map_generator import MapGenerator
from seeded_random import SeededRandom

def main():
    print("Hello, World!")
    print()

    # Не змінювати до повноцінної імплементації генератора карти
    grid_width = 21
    grid_height = 36

    generator = MapGenerator(grid_width, grid_height)
    map = generator.generate_map()
    map.print_map()
    

if __name__ == "__main__":
    main()