import state, pygame
from typing import Tuple, Any

class GameMenuConfig():
    '''Конфігурація меню гри'''
    def __init__(self):

        # default values
        screen_width: int = pygame.display.get_surface().get_width()
        screen_height: int = pygame.display.get_surface().get_height()

        self.button_size: Tuple[int, int] = (220, 60)
        self.input_seed_size: Tuple[int, int] = (300, 50)

        # Center positioning - map on top
        self.map_size: Tuple[int, int] = (350, 350)
        self.map_offsets: Tuple[int, int] = ((screen_width - 350) // 2, 40)

        # Input field centered, below map with proper spacing
        input_x: int = (screen_width - self.input_seed_size[0]) // 2
        self.input_seed_pos: Tuple[int, int] = (input_x, 420)
        self.label_y: int = 400

        # Buttons centered horizontally with more spacing
        self.start_btn_pos: Tuple[int, int] = (screen_width // 2, 530)
        self.back_btn_pos: Tuple[int, int] = (screen_width // 2, 620)

        self.backg_color: Tuple[int, int, int] = (0, 0, 0)
        self.seed_input_text_color: Tuple[int, int, int] = (255, 255, 255)

        self.font: str = "Arial"
        self.font_size: int = 40
        self.label_font_size: int = 28