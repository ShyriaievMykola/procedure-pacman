import pygame
from .colors import Colors as C
from .config import CameraConfig as CC, GraphicsConfig as GC
from constants import WALL, PELLET, POWER, FRUIT

class Visualizer:
    """
    Базовий клас для візуалізації гри Pac-Man на екрані.
    Керує віддаленням компонентів карти, пелетів, стін та камери для відображення ігрового світу.
    """
    def __init__(self, screen: pygame.Surface, map_gen: object) -> None:
        """
        Iniціалізація візуалізатора гри.
        Args:
            screen(pygame.Surface): pygame екран для рендеру
            map_gen(object): об'єкт генератора карти з інформацією про розміри та елементи карти
        Returns:
            None
        """
        self.screen = screen
        self.map = map_gen

        self.cell = self.screen.get_width() // map_gen.width
        self.x_offset = (self.screen.get_width() - (map_gen.width * self.cell)) // 2
        
        self.y = 0
        self.max_y = max(0, map_gen.height * self.cell - self.screen.get_height())
        self.speed = self.cell // CC.SPEED_DIVISOR

        self.texture_map = self.map.get_texture_map()
    
    def get_screen_pos(self, x: int, y: int) -> tuple:
        """
        Конвертує координати мапи у координати екрану з урахуванням зміщення камери.
        Args:
            x(int): X координата на мапі
            y(int): Y координата на мапі
        Returns:
            tuple: (sx, sy) координати для малювання на екрані
        """
        return (x * self.cell + self.x_offset, y * self.cell - self.y)
    
    def draw_cell(self, rect: pygame.Rect, color: tuple, border: int = 0) -> None:
        """
        Малює прямокутник комірки на екрані з вказаним кольором.
        Args:
            rect(pygame.Rect): Об'єкт прямокутника для малювання
            color(tuple): RGB колір для заповнення комірки
            border(int): Товщина контуру (0 для заповненого прямокутника)
        Returns:
            None
        """
        pygame.draw.rect(self.screen, color, rect, border)
    
    def draw_pellet(self, x: int, y: int, sx: int, sy: int, pellet_type: int) -> None:
        """
        Малює пелет відповідного типу (звичайний, сила, фрукт) на екрані.
        Args:
            x(int): X координата пелета на мапі
            y(int): Y координата пелета на мапі
            sx(int): X координата для малювання на екрані
            sy(int): Y координата для малювання на екрані
            pellet_type(int): Тип пелета (PELLET, POWER, або FRUIT)
        Returns:
            None
        """
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
    
    def draw_wall_borders(self, x: int, y: int, sx: int, sy: int) -> None:
        """
        Малює кордони стін з виділенням на основі текстурної мапи світу.
        Визначає, які сторони комірки повинні мати контур, залежно від сусідніх стін.
        Args:
            x(int): X координата стіни на мапі
            y(int): Y координата стіни на мапі
            sx(int): X координата для малювання на екрані
            sy(int): Y координата для малювання на екрані
        Returns:
            None
        """
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
    
    def draw_map_base(self, eaten_pellets: set = None) -> None:
        """
        Малює повну базову карту: стіни, двері, проходи та пелети, що залишилися.
        Ігнорує пелети, які були вже з'їдені (знаходяться у eaten_pellets).
        Args:
            eaten_pellets(set): Набір координат пелетів, які були вже з'їдені
        Returns:
            None
        """
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
    
    def _is_gh(self, x: int, y: int) -> bool:
        """
        Перевіряє, чи знаходиться позиція всередині будинку привидів.
        Args:
            x(int): X координата для перевірки
            y(int): Y координата для перевірки
        Returns:
            bool: True якщо позиція всередині будинку привидів, False інакше
        """
        gx, gy = self.map.ghost_x, self.map.ghost_y
        return gx[0] <= x <= gx[1] and gy[0] <= y <= gy[1]
