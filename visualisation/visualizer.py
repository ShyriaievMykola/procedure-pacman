import pygame
from .colors import Colors as C
from .config import CameraConfig as CC, GraphicsConfig as GC
from constants import WALL, PELLET, POWER, FRUIT

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

        self.texture_map = self.map.get_texture_map()
    
    def get_screen_pos(self, x, y):
        """Конвертує координати мапи у координати екрану"""
        return (x * self.cell + self.x_offset, y * self.cell - self.y)
    
    def draw_cell(self, rect, color, border=0):
        pygame.draw.rect(self.screen, color, rect, border)
    
    def draw_pellet(self, x, y, sx, sy, pellet_type):
        """Малює пелет відповідного типу"""
        if pellet_type == PELLET:
            # Звичайний пелет
            r = max(GC.MIN_DOT_SIZE, self.cell // GC.DOT_SIZE_DIVISOR)
            pygame.draw.circle(self.screen, C.DOT, (sx + self.cell//2, sy + self.cell//2), r)
        elif pellet_type == POWER:
            # Підсилення
            r = max(GC.MIN_DOT_SIZE, self.cell // GC.POWER_PELLET_SIZE_DIVISOR)
            pygame.draw.circle(self.screen, C.DOT, (sx + self.cell//2, sy + self.cell//2), r)
        elif pellet_type == FRUIT:
            # Фрукт
            r = max(GC.MIN_DOT_SIZE, self.cell // GC.POWER_PELLET_SIZE_DIVISOR)
            pygame.draw.circle(self.screen, (255, 100, 100), (sx + self.cell//2, sy + self.cell//2), r)
    
    def draw_wall_borders(self, x, y, sx, sy):
        """Малює кордони стін на основі текстурної мапи"""
        texture = self.texture_map[y][x]
        
        top_l = (sx, sy)
        top_r = (sx + self.cell, sy)
        bot_l = (sx, sy + self.cell)
        bot_r = (sx + self.cell, sy + self.cell)
        
        border_width = max(1, GC.WALL_BORDER_WIDTH)
        
        # Малюємо лінії тільки там, де немає сусідньої стіни
        if not texture & 1:  # Верх
            pygame.draw.line(self.screen, C.WALL_HIGHLIGHT, top_l, top_r, border_width)
        if not texture & 2:  # Право
            pygame.draw.line(self.screen, C.WALL_HIGHLIGHT, top_r, bot_r, border_width)
        if not texture & 4:  # Низ
            pygame.draw.line(self.screen, C.WALL_HIGHLIGHT, bot_l, bot_r, border_width)
        if not texture & 8:  # Ліво
            pygame.draw.line(self.screen, C.WALL_HIGHLIGHT, top_l, bot_l, border_width)
    
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
                    
                    if pos == self.map.ghost_door: 
                        self.draw_cell(rect, C.DOOR)
                    elif cell == WALL:
                        self.draw_cell(rect, C.WALL)
                        self.draw_wall_borders(x, y, sx, sy)
                    elif self._is_gh(x, y): 
                        self.draw_cell(rect, C.GHOST_HOUSE)
                    elif pos in (self.map.passage_left, self.map.passage_right):
                        self.draw_cell(rect, C.PASSAGE)
                    else:
                        # Малюємо пелети тільки якщо вони є в pellet_grid і не з'їдені
                        if pos not in eaten:
                            pellet_type = self.map.pellet_grid[y][x]
                            if pellet_type in (PELLET, POWER, FRUIT):
                                self.draw_pellet(x, y, sx, sy, pellet_type)
    
    def _is_gh(self, x, y):
        gx, gy = self.map.ghost_x, self.map.ghost_y
        return gx[0] <= x <= gx[1] and gy[0] <= y <= gy[1]