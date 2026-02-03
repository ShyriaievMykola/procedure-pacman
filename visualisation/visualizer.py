import pygame
import sys
from .colors import Colors as C
from .config import CameraConfig as CC, GraphicsConfig as GC
from constants import WALL

class Visualizer:
    def __init__(self, map_gen):
        pygame.init()
        self.map = map_gen
        
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()
        
        # Розмір комірки базується на ширині екрану, щоб карта помістилася по горизонталі
        self.cell = screen_width // map_gen.width
        
        # Центруємо карту по горизонталі, якщо є зайве місце
        total_map_width = map_gen.width * self.cell
        self.x_offset = (screen_width - total_map_width) // 2
        
        self.y, self.vel = 0, 0
        self.max_y = max(0, map_gen.height * self.cell - screen_height)
        self.speed = self.cell // CC.SPEED_DIVISOR
        
    def _draw_points(self, x, y, sx, sy):
        is_p = (x in (1, self.map.width-2) and y in (1, self.map.height-2))
        div = GC.POWER_PELLET_SIZE_DIVISOR if is_p else GC.DOT_SIZE_DIVISOR
        min_s = GC.MIN_POWER_PELLET_SIZE if is_p else GC.MIN_DOT_SIZE
        
        r = max(min_s, self.cell // div)
        pygame.draw.circle(self.screen, C.DOT, (sx + self.cell//2, sy + self.cell//2), r)
        
    def draw(self):
        self.screen.fill(C.TUNNEL)
        sh = self.screen.get_height()
        
        for y in range(self.map.height):
            sy = y * self.cell - self.y
            # Рендеримо тільки те, що потрапляє в зону видимості екрана
            if -self.cell < sy < sh:
                for x in range(self.map.width):
                    sx = x * self.cell + self.x_offset
                    rect = pygame.Rect(sx, sy, self.cell, self.cell)
                    cell, pos = self.map.grid[y][x], (x, y)
                    
                    # Вхід в гост хаус
                    if pos == self.map.ghost_door:
                        pygame.draw.rect(self.screen, C.DOOR, rect)
                    
                    # Стіни
                    elif cell == WALL:
                        pygame.draw.rect(self.screen, C.WALL, rect)
                        pygame.draw.rect(self.screen, C.WALL_HIGHLIGHT, rect, GC.WALL_BORDER_WIDTH)
                    
                    # Зона гост хаусу
                    elif self._is_gh(x, y):
                        pygame.draw.rect(self.screen, C.GHOST_HOUSE, rect)
                    
                    # Телепорти
                    elif pos in (self.map.passage_left, self.map.passage_right):
                        pygame.draw.rect(self.screen, C.PASSAGE, rect)
                    
                    # Точки
                    else:
                        self._draw_points(x, y, sx, sy)
                        
        pygame.display.flip()
        
    def _is_gh(self, x, y):
        gx, gy = self.map.ghost_x, self.map.ghost_y
        return gx[0] <= x <= gx[1] and gy[0] <= y <= gy[1]
        
    def run(self):
        clock = pygame.time.Clock()
        while True:
            for e in pygame.event.get():
                if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
                    pygame.quit(); sys.exit()
                    
            keys = pygame.key.get_pressed()
            target = (keys[pygame.K_s] - keys[pygame.K_w]) * self.speed
            
            if target: self.vel += (target - self.vel) * CC.ACCELERATION
            else: self.vel *= CC.FRICTION
            
            if abs(self.vel) < CC.MIN_VELOCITY: self.vel = 0
            self.y = max(0, min(self.max_y, self.y + self.vel))
            
            self.draw()
            clock.tick(60)