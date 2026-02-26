import pygame

from menus.main.config import DifficultyConfig
import state

class DifficultyMenu:
    """
    Меню вибору складності гри
    Attributes:
        cfg (DifficultyConfig): Конфігурація меню складності
        font (pygame.font.Font): Шрифт для відображення тексту
        button_size (tuple): Розмір кнопок
        buttons (list): Список кнопок з їх текстом, позицією та дією
    """
    def __init__(self):
        self.cfg = DifficultyConfig()
        self.font = pygame.font.SysFont(self.cfg.font, 40, bold=True)

        self.button_size = self.cfg.button_size
        button_start_x = (state.game_instance.screen.get_width() - self.button_size[0]) // 2
        self.buttons = [
            {
                'text': 'EASY',
                'rect': pygame.Rect(button_start_x, 200, *self.button_size),
                'action': 'SET_EASY'
            },

            {
                'text': 'MEDIUM',
                'rect': pygame.Rect(button_start_x, 300, *self.button_size),
                'action': 'SET_MEDIUM'
            },
            {
                'text': 'HARD',
                'rect': pygame.Rect(button_start_x, 400, *self.button_size),
                'action': 'SET_HARD'
            }
        ]

    def draw(self):
        """
        Функція для відображення меню вибору складності на екрані. 
        Вона очищує екран, отримує позицію миші та відображає кнопки з 
        відповідними кольорами залежно від того, чи знаходиться курсор над ними.
        """
        state.game_instance.screen.fill((0, 0, 0))
        mouse_pos = pygame.mouse.get_pos()
        for btn in self.buttons:
            btn_color  = (255, 255, 0) if btn['rect'].collidepoint(mouse_pos) else (180, 180, 180)
            pygame.draw.rect(state.game_instance.screen, (0,0,0), btn['rect'], border_radius=10)
            text = self.font.render(btn['text'], True, btn_color)
            state.game_instance.screen.blit(text, text.get_rect(center=btn['rect'].center))

    def handle_event(self, event):
        """
        Функція для обробки подій, пов'язаних з меню вибору складності.
        Вона перевіряє, чи була натиснута ліва кнопка миші, і якщо так, то перевіряє, 
        чи курсор знаходиться над будь-якою з кнопок.
        Args:
            event (pygame.event.Event): Подія, яку потрібно обробити
        Returns:
            str або None: Дію, пов'язану з кнопкою, якщо вона була натиснута, або None, якщо ні
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for btn in self.buttons:
                if btn['rect'].collidepoint(event.pos):
                    return btn['action']
        return None