import pygame
import sys
import math
import pacman
from .visualizer import Visualizer
from .colors import Colors as C
from .config import CameraConfig as CC, GraphicsConfig as GC, GameConfig as G
from constants import WALL, TUNNEL

class PacManVisualizer(Visualizer):
    def __init__(self, map_gen):
        super().__init__(map_gen)
        self.font = pygame.font.Font(None, GC.TEXT_FONT_SIZE)
        self.eaten_pellets = set()
        self.move_timer = 0
        
        pacman.position = pacman.get_spawn_position(map_gen.grid)
        self.prev_pos = list(pacman.position)
        self.render_pos = list(pacman.position)
        
        pacman.movement_direction = (0, 0)
        pacman.pending_direction = (0, 0)
        pacman.points = 0

    def update_logic(self, dt):
        self.move_timer += dt
        
        # Розраховуємо коефіцієнт прогресу від 0.0 до 1.0 між клітинками
        progress = min(1.0, self.move_timer / G.PACMAN_SPEED_MS)
        
        # Плавна інтерполяція: render = стара_позиція + (різниця * прогрес)
        for i in range(2):
            diff = pacman.position[i] - self.prev_pos[i]
            if abs(diff) > 2: # Телепорт
                self.render_pos[i] = pacman.position[i]
            else:
                self.render_pos[i] = self.prev_pos[i] + (diff * progress)

        if self.move_timer >= G.PACMAN_SPEED_MS:
            self.prev_pos = list(pacman.position)
            pacman.resolve_pend(self.map.grid)
            
            px, py = pacman.position
            if self.map.grid[py][px] == TUNNEL and (px, py) not in self.eaten_pellets:
                self.eaten_pellets.add((px, py))
                pacman.points += 1
            
            self.move_timer = 0

    def update_camera(self):
        sh = self.screen.get_height()
        ideal_y = self.render_pos[1] * self.cell - (sh // 2)
        target_cam = max(0, min(self.max_y, ideal_y))
        self.y += (target_cam - self.y) * G.CAMERA_SMOOTHING

    def draw_pacman(self):
        sx = self.render_pos[0] * self.cell + self.x_offset + self.cell // 2
        sy = self.render_pos[1] * self.cell - self.y + self.cell // 2
        center = (sx, sy)
        radius = self.cell // 2 - G.PACMAN_RADIUS_OFFSET
        
        dirs = {(1,0): 0, (-1,0): 180, (0,-1): 90, (0,1): 270}
        rot = dirs.get(pacman.movement_direction, 0)
        
        is_open = (pygame.time.get_ticks() // G.MOUTH_ANIM_SPEED) % 2
        angle = 45 if is_open and pacman.movement_direction != (0,0) else 10
        
        pts = [center]
        for i in range(33):
            theta = math.radians(rot + angle + i * (360 - 2*angle)/32)
            pts.append((center[0] + radius * math.cos(theta), center[1] - radius * math.sin(theta)))
        pygame.draw.polygon(self.screen, C.PACMAN, pts)

    def run(self):
        clock = pygame.time.Clock()
        while True:
            dt = clock.tick(60)
            for e in pygame.event.get():
                if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
                    pygame.quit(); sys.exit()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_w] or keys[pygame.K_UP]: pacman.pending_direction = (0, -1)
            elif keys[pygame.K_s] or keys[pygame.K_DOWN]: pacman.pending_direction = (0, 1)
            elif keys[pygame.K_a] or keys[pygame.K_LEFT]: pacman.pending_direction = (-1, 0)
            elif keys[pygame.K_d] or keys[pygame.K_RIGHT]: pacman.pending_direction = (1, 0)

            self.update_logic(dt)
            self.update_camera()
            self.draw_map_base(self.eaten_pellets)
            self.draw_pacman()
            
            score = self.font.render(f"SCORE: {pacman.points}", True, C.SCORE_TEXT)
            self.screen.blit(score, (GC.TEXT_MARGIN, GC.TEXT_MARGIN))
            pygame.display.flip()