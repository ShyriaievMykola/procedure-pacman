import pygame
from .colors import Colors as C
from .config import GameConfig as G
from ghosts.behaviors.frightened_behavior import FrightenedBehavior
from ghosts.behaviors.eaten_behavior import EatenBehavior
import pacman

class GhostVisualizer:
    """
    Клас для візуалізації привидів на екрані гри.
    Керує рендеренням привидів з урахуванням їхніх поточних позицій, станів та напрямків руху.
    """
    
    def __init__(self, visualizer: object, ghost_manager: object) -> None:
        """
        Ініціалізація візуалізатора привидів.
        Args:
            visualizer(object): Об'єкт основного візуалізатора гри
            ghost_manager(object): Менеджер привидів, що містить список усіх привидів
        Returns:
            None
        """
        self.vis = visualizer
        self.ghosts = ghost_manager.ghosts
        self.prev_pos = {g: list(g.position) for g in self.ghosts}
        self.render_pos = {g: list(g.position) for g in self.ghosts}
        
        self.colors = {
            "red": C.GHOST_RED, "pink": C.GHOST_PINK,
            "blue": C.GHOST_BLUE, "orange": C.GHOST_ORANGE
        }
    
    def update_positions(self, progress: float) -> None:
        """
        Оновлює позиції привидів для плавної анімації їхнього руху.
        Обчислює позицію рендеру на основі прогресу між попередньою та поточною позицією.
        Args:
            progress(float): Значення від 0 до 1, що визначає прогрес анімації переміщення
        Returns:
            None
        """
        for g in self.ghosts:
            for i in range(2):
                diff = g.position[i] - self.prev_pos[g][i]
                if abs(diff) > 2:  # Телепорт
                    self.render_pos[g][i] = g.position[i]
                else:
                    self.render_pos[g][i] = self.prev_pos[g][i] + (diff * progress)
    
    def save_positions(self) -> None:
        """
        Зберігає поточні позиції всіх привидів як попередні позиції для наступної анімації.
        Args:
            None
        Returns:
            None
        """
        for g in self.ghosts:
            self.prev_pos[g] = list(g.position)
    
    def draw_ghosts(self) -> None:
        """
        Малює всіх привидів на екрані гри з урахуванням їхніх станів та напрямків.
        Малює тіло привида, ніжки та очі з обрахуванням правильного кольору залежно від поточного стану
        (звичайна режим, наляканий або з'їдений привід).
        Args:
            None
        Returns:
            None
        """
        for g in self.ghosts:
            pos = self.render_pos[g]
            sx = pos[0] * self.vis.cell + self.vis.x_offset + self.vis.cell // 2
            sy = pos[1] * self.vis.cell - self.vis.y + self.vis.cell // 2
            r = self.vis.cell // 2 - G.PACMAN_RADIUS_OFFSET
            
            # Колір
            if isinstance(g.strategy, FrightenedBehavior):
                color = C.GHOST_FRIGHTENED_BLINK if (pygame.time.get_ticks() // G.GHOST_FRIGHTENED_BLINK_SPEED) % 2 and pacman.almost_lost_power else C.GHOST_FRIGHTENED
            elif isinstance(g.strategy, EatenBehavior):
                color = C.GHOST_EATEN
            else:
                color = self.colors.get(g.color, C.GHOST_RED)
            
            # Тіло
            pygame.draw.circle(self.vis.screen, color, (sx, sy), r)
            pygame.draw.rect(self.vis.screen, color, (sx - r, sy, r * 2, r))
            
            # Ніжки
            w = r * 2 // G.GHOST_WAVE_COUNT
            pts = [(sx - r + i * w, sy + r + (w // G.GHOST_WAVE_HEIGHT_DIVISOR if i % 2 else 0)) 
                   for i in range(G.GHOST_WAVE_COUNT + 1)]
            pts += [(sx + r, sy + r), (sx + r, sy), (sx - r, sy)]
            pygame.draw.polygon(self.vis.screen, color, pts)
            
            # Очі
            if not isinstance(g.strategy, EatenBehavior):
                dx, dy = getattr(g, 'movement_direction', (0, 0))
                ey = sy - r // G.GHOST_EYE_OFFSET_Y_DIVISOR
                er = r // G.GHOST_EYE_RADIUS_DIVISOR
                pr = er // G.GHOST_PUPIL_RADIUS_DIVISOR
                po = (dx * er // G.GHOST_PUPIL_MOVE_DIVISOR, dy * er // G.GHOST_PUPIL_MOVE_DIVISOR)
                
                for ex in [sx - r // G.GHOST_EYE_OFFSET_X_DIVISOR, sx + r // G.GHOST_EYE_OFFSET_X_DIVISOR]:
                    pygame.draw.circle(self.vis.screen, C.GHOST_EYE_WHITE, (ex, ey), er)
                    pygame.draw.circle(self.vis.screen, C.GHOST_EYE_PUPIL, (ex + po[0], ey + po[1]), pr)