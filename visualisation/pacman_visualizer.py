import pygame, sys, math, pacman
from .visualizer import Visualizer
from .colors import Colors as C
from .config import GameConfig as G, GraphicsConfig as GC
from constants import WALL, TUNNEL

class PacManVisualizer(Visualizer):
    def __init__(self, map_gen):
        super().__init__(map_gen)
        self.font = pygame.font.Font(C.UI_FONT, GC.TEXT_FONT_SIZE)
        self.eaten_pellets = set()
        self.move_timer = 0
        
        pacman.position = pacman.get_spawn_position(map_gen.grid)
        pacman.movement_direction = pacman.pending_direction = (0, 0)
        pacman.points = 0

    def draw_pacman(self):
        sx, sy = self.get_screen_pos(*pacman.position)
        center = (sx + self.cell // 2, sy + self.cell // 2)
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

    def update_camera(self):
        _, py = self.get_screen_pos(*pacman.position)
        sh = self.screen.get_height()
        margin = sh * G.CAMERA_MARGIN_PCT
        
        target = self.y
        if py > sh - margin: target = pacman.position[1] * self.cell - sh + margin
        elif py < margin: target = pacman.position[1] * self.cell - margin
        
        self.y += (max(0, min(self.max_y, target)) - self.y) * G.CAMERA_SMOOTHING

    def run(self):
        clock = pygame.time.Clock()
        while True:
            dt = clock.tick(60)
            for e in pygame.event.get():
                if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
                    pygame.quit(); sys.exit()

            # Введення
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]: pacman.pending_direction = (0, -1)
            elif keys[pygame.K_s]: pacman.pending_direction = (0, 1)
            elif keys[pygame.K_a]: pacman.pending_direction = (-1, 0)
            elif keys[pygame.K_d]: pacman.pending_direction = (1, 0)

            # Логіка руху
            self.move_timer += dt
            if self.move_timer >= G.PACMAN_SPEED_MS:
                pacman.resolve_pend(self.map.grid)
                # Перевірка їжі
                px, py = pacman.position
                if self.map.grid[py][px] == TUNNEL and (px, py) not in self.eaten_pellets:
                    self.eaten_pellets.add((px, py))
                    pacman.points += 1
                self.move_timer = 0

            self.update_camera()
            self.draw_map_base(self.eaten_pellets)
            self.draw_pacman()
            
            # UI
            score = self.font.render(f"Score: {pacman.points}", True, C.SCORE_TEXT)
            self.screen.blit(score, (GC.TEXT_MARGIN, GC.TEXT_MARGIN))
            pygame.display.flip()