import pygame
from menus.main.config import MainMenuConfig
import state

class MainMenu:
    def __init__(self):
        self.mmc = MainMenuConfig()
        self.title_font = pygame.font.SysFont("Arial", 120, bold=True)
        self.subtitle_font = pygame.font.SysFont("Arial", 24)
        self.button_font = pygame.font.SysFont("Arial", 50, bold=True)

        screen_width = state.game_instance.screen.get_width()
        
        self.buttons = [
            {
                'text': 'BEGIN',
                'pos': (screen_width // 2, 380),
                'action': 'GO_TO_SEED'
            },
            {
                'text': 'QUIT',
                'pos': (screen_width // 2, 480),
                'action': 'QUIT'
            }
        ]

    def draw(self):
        state.game_instance.screen.fill((0, 0, 0))
        
        screen_width = state.game_instance.screen.get_width()
        screen_height = state.game_instance.screen.get_height()
        
        # Малюємо заголовок PACMAN
        title_text = self.title_font.render("PACMAN", True, (255, 255, 0))
        title_rect = title_text.get_rect(center=(screen_width // 2, 120))
        state.game_instance.screen.blit(title_text, title_rect)
        
        # Малюємо підпис procedure
        subtitle_text = self.subtitle_font.render("procedure", True, (200, 200, 200))
        subtitle_rect = subtitle_text.get_rect(center=(screen_width // 2, 200))
        state.game_instance.screen.blit(subtitle_text, subtitle_rect)
        
        mouse_pos = pygame.mouse.get_pos()
        
        # Малюємо кнопки (тільки текст)
        for btn in self.buttons:
            color = (255, 255, 0) if self._is_button_hovered(btn, mouse_pos) else (150, 150, 150)
            text_surf = self.button_font.render(btn['text'], True, color)
            text_rect = text_surf.get_rect(center=btn['pos'])
            state.game_instance.screen.blit(text_surf, text_rect)

    def _is_button_hovered(self, btn, mouse_pos):
        text_surf = self.button_font.render(btn['text'], True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=btn['pos'])
        return text_rect.collidepoint(mouse_pos)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for btn in self.buttons:
                if self._is_button_hovered(btn, event.pos):
                    return btn['action']
        return None