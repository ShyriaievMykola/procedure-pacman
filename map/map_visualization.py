import pygame
from constants import *
from map.config import MapGeneratorConfig as cfg
class MapVisualization:
    
    @staticmethod
    def display_map(map, cell_size = 20):
        pygame.init()
        
        screen_width = map.width * cell_size
        screen_height = map.height * cell_size

        screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Procedural Pac-Man Maze Map Test")
        clock = pygame.time.Clock()

        running = True
        while running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
            MapVisualization.render(map, screen, cell_size)
            pygame.display.flip()
            clock.tick(60) 
        
        pygame.quit()

    @staticmethod
    def render(map, screen, cell_size):
        for y in range(map.height):
            for x in range(map.width):
                rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
                
                if (map.ghost_x[0] <= x <= map.ghost_x[1] and map.ghost_y[0] <= y <= map.ghost_y[1]):
                    color = (255, 0, 0)
                elif (x, y) == map.ghost_door:
                    color = (0, 255, 0)
                elif (x, y) == map.passage_left or (x, y) == map.passage_right:
                    color = (0, 0, 255)
                elif map.grid[y][x] == WALL:
                    color = (0, 0, 0)
                else:
                    color = (100, 100, 100)

                pygame.draw.rect(screen, color, rect)
                
                if (map.pellet_grid[y][x] == PELLET):
                    ux = x*cell_size + cell_size//2
                    uy = y*cell_size + cell_size//2
                    pygame.draw.circle(screen, (255, 255, 0), (ux, uy), 3)
                elif (map.pellet_grid[y][x] == FRUIT):
                    ux = x*cell_size + cell_size//2
                    uy = y*cell_size + cell_size//2
                    pygame.draw.circle(screen, (0, 255, 0), (ux, uy), 3)
                elif (map.pellet_grid[y][x] == POWER):
                    ux = x*cell_size + cell_size//2
                    uy = y*cell_size + cell_size//2
                    pygame.draw.circle(screen, (255, 205, 0), (ux, uy), 6)
                
                if (map.untouchable_zones[y][x] == True and cfg.DEBUG_VIEW):
                    ux = x*cell_size + cell_size//2
                    uy = y*cell_size + cell_size//2
                    pygame.draw.circle(screen, (255, 0, 0), (ux, uy), 2)