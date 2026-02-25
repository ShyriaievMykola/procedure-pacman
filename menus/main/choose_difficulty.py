import pygame

from menus.main.config import DifficultyConfig
import state

class DifficultyMenu:
    def __init__(self):
        self.cfg = DifficultyConfig()
        self.font = pygame.font.SysFont(self.cfg.font, self.cfg.font_size)

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
        state.game_instance.screen.fill((30, 30, 30))
        mouse_pos = pygame.mouse.get_pos()
        for btn in self.buttons:
            color = (170, 170, 170) if btn['rect'].collidepoint(mouse_pos) else (100, 100, 100)
            pygame.draw.rect(state.game_instance.screen, color, btn['rect'], border_radius=10)
            text_surf = self.font.render(btn['text'], True, (255, 255, 255))
            state.game_instance.screen.blit(text_surf, text_surf.get_rect(center=btn['rect'].center))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for btn in self.buttons:
                if btn['rect'].collidepoint(event.pos):
                    return btn['action']
        return None