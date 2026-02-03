import pygame
from .colors import Colors as C
from .config import CameraConfig as CC, GraphicsConfig as GC
from constants import WALL

class Visualizer:
    def __init__(self, map_gen):
        pygame.init()
        self.map = map_gen
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        
        self.cell = self.screen.get_width() // map_gen.width
        self.x_offset = (self.screen.get_width() - (map_gen.width * self.cell)) // 2
        
        self.y = 0
        self.max_y = max(0, map_gen.height * self.cell - self.screen.get_height())
        self.speed = self.cell // CC.SPEED_DIVISOR

    def get_screen_pos(self, x, y):
        """Конвертує координати мапи у координати екрану"""
        return (x * self.cell + self.x_offset, y * self.cell - self.y)

    def draw_cell(self, rect, color, border=0):
        pygame.draw.rect(self.screen, color, rect, border)

    def draw_pellet(self, x, y, sx, sy, is_eaten=False):
        if is_eaten: return
        is_p = (x in (1, self.map.width-2) and y in (1, self.map.height-2))
        div = GC.POWER_PELLET_SIZE_DIVISOR if is_p else GC.DOT_SIZE_DIVISOR
        r = max(GC.MIN_DOT_SIZE, self.cell // div)
        pygame.draw.circle(self.screen, C.DOT, (sx + self.cell//2, sy + self.cell//2), r)

    def draw_map_base(self, eaten_pellets=None):
        self.screen.fill(C.TUNNEL)
        eaten = eaten_pellets or set()
        
        for y in range(self.map.height):
            sx, sy = self.get_screen_pos(0, y)
            if -self.cell < sy < self.screen.get_height():
                for x in range(self.map.width):
                    sx, _ = self.get_screen_pos(x, y)
                    rect = pygame.Rect(sx, sy, self.cell, self.cell)
                    cell, pos = self.map.grid[y][x], (x, y)

                    if pos == self.map.ghost_door: self.draw_cell(rect, C.DOOR)
                    elif cell == WALL:
                        self.draw_cell(rect, C.WALL)
                        self.draw_cell(rect, C.WALL_HIGHLIGHT, GC.WALL_BORDER_WIDTH)
                    elif self._is_gh(x, y): self.draw_cell(rect, C.GHOST_HOUSE)
                    elif pos in (self.map.passage_left, self.map.passage_right):
                        self.draw_cell(rect, C.PASSAGE)
                    else:
                        self.draw_pellet(x, y, sx, sy, pos in eaten)

    def _is_gh(self, x, y):
        gx, gy = self.map.ghost_x, self.map.ghost_y
        return gx[0] <= x <= gx[1] and gy[0] <= y <= gy[1]