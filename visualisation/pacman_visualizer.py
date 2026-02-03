import pygame
import sys
import math
import pacman
from .visualizer import Visualizer
from constants import WALL, TUNNEL
from .config import CameraConfig as CC, GraphicsConfig as GC
from .colors import Colors as C

class PacManVisualizer:
    """Інтеграція логіки руху Pac-Man з візуалізатором"""
    
    def __init__(self, map_gen):
        self.map_gen = map_gen
        self.visualizer = Visualizer(map_gen)
        
        # Ініціалізуємо Pac-Man
        pacman.position = pacman.get_spawn_position(map_gen.grid)
        pacman.movement_direction = (0, 0)
        pacman.pending_direction = (0, 0)
        pacman.points = 0
        
        # Таймер для руху Pac-Man
        self.move_timer = 0
        self.move_delay = 200  # мілісекунди між рухами
        
        # Колір Pac-Man
        self.pacman_color = (255, 255, 0)  # Жовтий
        
        # Для плавної камери
        self.target_camera_y = 0
        self.camera_smooth_speed = 0.15  # Швидкість інтерполяції (0-1, менше = плавніше)
        
        # Відстеження з'їдених точок
        self.eaten_pellets = set()  # Множина координат з'їдених таблеток
        
    def draw_pacman(self):
        """Малює Pac-Man на екрані"""
        x, y = pacman.position
        sx = x * self.visualizer.cell + self.visualizer.x_offset + self.visualizer.cell // 2
        sy = y * self.visualizer.cell - self.visualizer.y + self.visualizer.cell // 2
        
        radius = self.visualizer.cell // 2 - 2
        
        # Визначаємо кут рота залежно від напрямку руху
        dx, dy = pacman.movement_direction
        
        # Кут обертання Pac-Man
        if dx == 1:  # Вправо
            rotation = 0
        elif dx == -1:  # Вліво
            rotation = 180
        elif dy == -1:  # Вгору
            rotation = 90
        elif dy == 1:  # Вниз
            rotation = 270
        else:  # Стоїть на місці
            rotation = 0
        
        # Анімація рота (відкриття/закриття)
        mouth_open = (pygame.time.get_ticks() // 100) % 2  # Мигає кожні 100мс
        mouth_angle = 45 if mouth_open and pacman.movement_direction != (0, 0) else 10
        
        # Малюємо Pac-Man як дугу (коло з вирізаним шматком)
        start_angle = math.radians(rotation + mouth_angle)
        end_angle = math.radians(rotation + 360 - mouth_angle)
        
        # Створюємо список точок для полігону
        points = [(sx, sy)]
        
        # Генеруємо точки дуги
        num_points = 32
        angle_step = (end_angle - start_angle) / num_points
        
        for i in range(num_points + 1):
            angle = start_angle + i * angle_step
            px = sx + radius * math.cos(angle)
            py = sy - radius * math.sin(angle)  # Мінус бо Y інвертований
            points.append((px, py))
        
        # Малюємо Pac-Man
        pygame.draw.polygon(self.visualizer.screen, self.pacman_color, points)
    
    def _draw_points(self, x, y, sx, sy):
        """Малює точки (таблетки) якщо вони не з'їдені"""
        # Перевіряємо чи таблетка не з'їдена
        if (x, y) in self.eaten_pellets:
            return  # Не малюємо з'їдені таблетки
            
        is_power = (x in (1, self.map_gen.width-2) and y in (1, self.map_gen.height-2))
        div = GC.POWER_PELLET_SIZE_DIVISOR if is_power else GC.DOT_SIZE_DIVISOR
        min_s = GC.MIN_POWER_PELLET_SIZE if is_power else GC.MIN_DOT_SIZE
        
        r = max(min_s, self.visualizer.cell // div)
        pygame.draw.circle(self.visualizer.screen, C.DOT, (sx + self.visualizer.cell//2, sy + self.visualizer.cell//2), r)
    
    def _is_ghost_house(self, x, y):
        """Перевіряє чи клітинка знаходиться в гост хаусі"""
        gx, gy = self.map_gen.ghost_x, self.map_gen.ghost_y
        return gx[0] <= x <= gx[1] and gy[0] <= y <= gy[1]
    
    def draw(self):
        """Малює весь ігровий екран"""
        self.visualizer.screen.fill(C.TUNNEL)
        screen_height = self.visualizer.screen.get_height()
        
        # Малюємо лабіринт
        for y in range(self.map_gen.height):
            sy = y * self.visualizer.cell - self.visualizer.y
            
            if -self.visualizer.cell < sy < screen_height:
                for x in range(self.map_gen.width):
                    sx = x * self.visualizer.cell + self.visualizer.x_offset
                    rect = pygame.Rect(sx, sy, self.visualizer.cell, self.visualizer.cell)
                    cell = self.map_gen.grid[y][x]
                    pos = (x, y)
                    
                    # Вхід в гост хаус
                    if pos == self.map_gen.ghost_door:
                        pygame.draw.rect(self.visualizer.screen, C.DOOR, rect)
                    
                    # Стіни
                    elif cell == WALL:
                        pygame.draw.rect(self.visualizer.screen, C.WALL, rect)
                        pygame.draw.rect(self.visualizer.screen, C.WALL_HIGHLIGHT, rect, GC.WALL_BORDER_WIDTH)
                    
                    # Зона гост хаусу
                    elif self._is_ghost_house(x, y):
                        pygame.draw.rect(self.visualizer.screen, C.GHOST_HOUSE, rect)
                    
                    # Телепорти
                    elif pos in (self.map_gen.passage_left, self.map_gen.passage_right):
                        pygame.draw.rect(self.visualizer.screen, C.PASSAGE, rect)
                    
                    # Точки (якщо не з'їдені)
                    else:
                        self._draw_points(x, y, sx, sy)
        
        # Малюємо Pac-Man
        self.draw_pacman()
        
        # Малюємо рахунок
        self.draw_score()
        
        pygame.display.flip()
    
    def draw_score(self):
        """Малює рахунок на екрані"""
        font = pygame.font.Font(None, 48)
        score_text = font.render(f"Score: {pacman.points}", True, (255, 255, 255))
        lives_text = font.render(f"Lives: 3", True, (255, 255, 255))
        
        self.visualizer.screen.blit(score_text, (20, 20))
        self.visualizer.screen.blit(lives_text, (20, 70))
    
    def handle_pacman_input(self):
        """Обробляє введення для керування Pac-Man"""
        keys = pygame.key.get_pressed()
        
        # Використовуємо стрілки для керування Pac-Man
        if keys[pygame.K_w]:
            pacman.pending_direction = (0, -1)
        elif keys[pygame.K_s]:
            pacman.pending_direction = (0, 1)
        elif keys[pygame.K_a]:
            pacman.pending_direction = (-1, 0)
        elif keys[pygame.K_d]:
            pacman.pending_direction = (1, 0)
    
    def update_camera_follow_pacman(self):
        """Автоматично скролить камеру за Pac-Man з плавною анімацією"""
        screen_height = self.visualizer.screen.get_height()
        pacman_screen_y = pacman.position[1] * self.visualizer.cell - self.visualizer.y
        
        # Якщо Pac-Man виходить за межі екрану - оновлюємо цільову позицію камери
        margin = screen_height * 0.3  # 30% від висоти екрану
        
        if pacman_screen_y > screen_height - margin:
            # Pac-Man внизу екрану - скролимо вниз
            self.target_camera_y = pacman.position[1] * self.visualizer.cell - screen_height + margin
        elif pacman_screen_y < margin:
            # Pac-Man вгорі екрану - скролимо вгору
            self.target_camera_y = pacman.position[1] * self.visualizer.cell - margin
        
        # Обмежуємо цільову позицію
        self.target_camera_y = min(self.visualizer.max_y, max(0, self.target_camera_y))
        
        # Плавна інтерполяція до цільової позиції
        self.visualizer.y += (self.target_camera_y - self.visualizer.y) * self.camera_smooth_speed
    
    def check_pellet_eaten(self):
        """Перевіряє чи Pac-Man з'їв таблетку"""
        x, y = pacman.position
        # Перевіряємо чи є таблетка (не стіна і не порожній тунель)
        cell = self.map_gen.grid[y][x]
        if cell != WALL and cell == TUNNEL and (x, y) not in self.eaten_pellets:
            # Позначаємо що таблетка з'їдена
            self.eaten_pellets.add((x, y))
            pacman.points += 1
    
    def run(self):
        """Головний ігровий цикл"""
        clock = pygame.time.Clock()
        
        while True:
            delta_time = clock.tick(60)
            
            # Обробка подій
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()
            
            # Обробка введення
            self.handle_pacman_input()
            
            # Оновлення руху Pac-Man
            self.move_timer += delta_time
            if self.move_timer >= self.move_delay:
                pacman.resolve_pend(self.map_gen.grid)
                self.check_pellet_eaten()
                self.move_timer = 0
            
            # Оновлення камери (автоматичне слідкування за Pac-Man)
            self.update_camera_follow_pacman()
            
            # Малювання
            self.draw()
