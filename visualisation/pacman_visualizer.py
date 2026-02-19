import pygame
import sys
import math
import pacman
from .visualizer import Visualizer
from .colors import Colors as C
from .config import CameraConfig as CC, GraphicsConfig as GC, GameConfig as G
from constants import WALL, TUNNEL
from ghosts.ghost_manager import GhostManager
from .ghost_visualizer import GhostVisualizer
from ghosts.behaviors.eaten_behavior import EatenBehavior

class PacManVisualizer(Visualizer):
    def __init__(self, screen, map_gen):
        super().__init__(screen, map_gen)
        self.font = pygame.font.Font(None, GC.TEXT_FONT_SIZE)
        self.eaten_pellets = set()
        
        # Таймери
        self.pacman_timer = 0
        self.ghost_timer = 0
        
        # Ініціалізація Pac-Man (запам'ятовуємо фіксований спавн)
        self.spawn_pos = pacman.get_spawn_position(map_gen)
        pacman.position = self.spawn_pos
        self.prev_pos = list(self.spawn_pos)
        self.render_pos = list(self.spawn_pos)
        pacman.movement_direction = (0, 0)
        pacman.pending_direction = (0, 0)
        pacman.points = 0
        
        # Ініціалізація привидів
        self.ghost_manager = GhostManager(map_gen)
        self.ghost_viz = GhostVisualizer(self, self.ghost_manager)
        
        # Змінні циклу гри
        self.clock = pygame.time.Clock()
        self.running = True
        self.prev_health = pacman.health
        self.death_anim_playing = False
        self.death_anim_time = 0
        self.DEATH_ANIM_DURATION = 1200  # мс
        self.DEATH_ANIM_GAME_OVER_DURATION = 2000  # мс для останнього життя
        self.death_anim_game_over = False
        self.death_anim_target_duration = self.DEATH_ANIM_DURATION
        self.reset_after_death = False
    
    def update_logic(self, dt):
        self.pacman_timer += dt
        self.ghost_timer += dt
        if self.death_anim_playing:
            self.death_anim_time += dt
            if self.death_anim_time >= self.death_anim_target_duration:
                # Анімація завершилась — виконуємо скидання після анімації, якщо потрібно
                if self.reset_after_death:
                    pacman.position = self.spawn_pos
                    self.prev_pos = list(self.spawn_pos)
                    self.render_pos = list(self.spawn_pos)
                    pacman.movement_direction = (0, 0)
                    pacman.pending_direction = (0, 0)
                    self.ghost_manager.reset_ghosts()
                    self.reset_after_death = False

                self.death_anim_playing = False
                self.death_anim_time = 0
            # Під час анімації смерті призупиняємо керування та оновлення Pac-Man
            pacman.movement_direction = (0, 0)
            pacman.pending_direction = (0, 0)
            return
        
        # Прогрес анімації Pac-Man
        pacman_progress = min(1.0, self.pacman_timer / G.PACMAN_SPEED_MS)
        for i in range(2):
            diff = pacman.position[i] - self.prev_pos[i]
            if abs(diff) > 2:  # Телепортація
                self.render_pos[i] = pacman.position[i]
            else:
                self.render_pos[i] = self.prev_pos[i] + (diff * pacman_progress)
        
        # Прогрес анімації для привидів
        ghost_progress = min(1.0, self.ghost_timer / G.GHOST_SPEED_MS)
        self.ghost_viz.update_positions(ghost_progress)
        
        pacman.control()
        
        # Оновлення Pac-Man
        if self.pacman_timer >= G.PACMAN_SPEED_MS:
            self.prev_pos = list(pacman.position)
            pacman.update(self.map)
            
            px, py = pacman.position
            if self.map.grid[py][px] == TUNNEL and (px, py) not in self.eaten_pellets:
                self.eaten_pellets.add((px, py))
            
            self.pacman_timer = 0
        
        # Оновлення привидів
        if self.ghost_timer >= G.GHOST_SPEED_MS:
            self.ghost_viz.save_positions()
            self.ghost_manager.update(pacman)
            self.ghost_timer = 0
        
        # Колізія з привидами
        self.check_ghost_collisions()
    
    def update_camera(self):
        sh = self.screen.get_height()
        ideal_y = self.render_pos[1] * self.cell - (sh // 2)
        target_cam = max(0, min(self.max_y, ideal_y))
        self.y += (target_cam - self.y) * G.CAMERA_SMOOTHING
    
    def check_ghost_collisions(self):
        for ghost in self.ghost_manager.ghosts:
            if pacman.position == ghost.position:
                if not isinstance(ghost.strategy, EatenBehavior):
                    ghost_eaten = pacman.touch_ghost(ghost)
                    if ghost_eaten:
                        if not ghost.eaten_in_this_power_up:
                            pacman.eat_ghost()
                            ghost.eaten_in_this_power_up = True
                        self.ghost_manager.be_eaten(ghost)
        
        if not pacman.empowered:
            for ghost in self.ghost_manager.ghosts:
                ghost.eaten_in_this_power_up = False
        
        if pacman.health < self.prev_health:
            # Втрата життя — запускаємо анімацію на поточній позиції
            if pacman.health > 0:
                    # Нефінальна втрата життя: відтворити анімацію смерті, потім скинути на фіксований спавн
                self.death_anim_playing = True
                self.death_anim_time = 0
                self.death_anim_game_over = False
                self.death_anim_target_duration = self.DEATH_ANIM_DURATION
                self.reset_after_death = True
            else:
                # Фінальна втрата життя: відтворити анімацію Game Over на поточній позиції
                self.death_anim_playing = True
                self.death_anim_time = 0
                self.death_anim_game_over = True
                self.death_anim_target_duration = self.DEATH_ANIM_GAME_OVER_DURATION
        
        self.prev_health = pacman.health
    
    def draw_pacman(self):
        sx = self.render_pos[0] * self.cell + self.x_offset + self.cell // 2
        sy = self.render_pos[1] * self.cell - self.y + self.cell // 2
        center = (sx, sy)
        radius = self.cell // 2 - G.PACMAN_RADIUS_OFFSET
        
        dirs = {(1, 0): 0, (-1, 0): 180, (0, -1): 90, (0, 1): 270}
        rot = dirs.get(pacman.movement_direction, 0)
        
        if self.death_anim_playing:
            prog = min(1.0, self.death_anim_time / max(1, self.DEATH_ANIM_DURATION))
            if prog < 0.6:
                mouth_angle = 10 + (prog / 0.6) * 170
                scale = 1.0
            else:
                mouth_angle = 180
                scale = max(0.0, 1.0 - (prog - 0.6) / 0.4)

            rot_offset = prog * 720

            w = int(radius * 2 + 6)
            h = int(radius * 2 + 6)
            surf = pygame.Surface((w, h), pygame.SRCALPHA)
            local_center = (w // 2, h // 2)

            alpha = int(255 * (1.0 - prog))
            draw_radius = max(1, int(radius * scale))

            pts = [local_center]
            for i in range(33):
                theta = math.radians(rot + rot_offset + mouth_angle + i * (360 - 2 * mouth_angle) / 32)
                pts.append((local_center[0] + draw_radius * math.cos(theta), local_center[1] - draw_radius * math.sin(theta)))

            color = C.PACMAN + (alpha,) if isinstance(C.PACMAN, tuple) and len(C.PACMAN) == 3 else C.PACMAN
            pygame.draw.polygon(surf, color, pts)
            self.screen.blit(surf, (center[0] - w // 2, center[1] - h // 2))
            return

        is_open = (pygame.time.get_ticks() // G.MOUTH_ANIM_SPEED) % 2
        angle = 45 if is_open and pacman.movement_direction != (0, 0) else 10

        pts = [center]
        for i in range(33):
            theta = math.radians(rot + angle + i * (360 - 2 * angle) / 32)
            pts.append((center[0] + radius * math.cos(theta), center[1] - radius * math.sin(theta)))

        pygame.draw.polygon(self.screen, C.PACMAN, pts)
    
    def run_one_frame(self):
        dt = self.clock.tick(60)
        pygame.event.recent = pygame.event.get()
        for e in pygame.event.recent:
            if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
                self.running = False
                break
        
        self.update_logic(dt)
        self.update_camera()
        # Always draw current frame (including death animation if playing)
        self.draw_map_base(self.eaten_pellets)
        self.ghost_viz.draw_ghosts()
        self.draw_pacman()
        
        score = self.font.render(f"SCORE: {pacman.points}", True, C.SCORE_TEXT)
        self.screen.blit(score, (GC.TEXT_MARGIN, GC.TEXT_MARGIN))
        
        health = self.font.render(f"HEALTH: {pacman.health}", True, C.SCORE_TEXT)
        self.screen.blit(health, (GC.TEXT_MARGIN, GC.TEXT_MARGIN + GC.TEXT_FONT_SIZE + 10))

        # If player has no health, wait for game-over death animation (if any) to finish
        if pacman.health <= 0:
            if self.death_anim_game_over:
                if self.death_anim_playing:
                    return None
                else:
                    # finished final death animation -> clear flag and signal game over
                    self.death_anim_game_over = False
                    return 'GAME_OVER'
            else:
                return 'GAME_OVER'

        return None
    
    def run(self):
        while self.running:
            result = self.run_one_frame()
            if result == 'GAME_OVER':
                return 'GAME_OVER'
            pygame.display.flip()