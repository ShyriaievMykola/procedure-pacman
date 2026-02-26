import pygame
import state
from typing import Tuple, Any

class GameOverMenu:
    '''Меню завершення гри'''
    def __init__(self):
        self.font = pygame.font.SysFont("Arial", 80)
        self.button_font = pygame.font.SysFont("Arial", 50, bold=True)
        
        screen_width = state.game_instance.screen.get_width()
        screen_height = state.game_instance.screen.get_height()
        
        self.button_pos = (screen_width // 2, screen_height // 2 + 100)

    def draw(self) -> None:
        '''Відображення меню завершення гри'''
        state.game_instance.screen.fill((0, 0, 0))
        
        game_over_text = self.font.render("GAME OVER", True, (255, 100, 100))
        game_over_rect = game_over_text.get_rect(center=(
            state.game_instance.screen.get_width() // 2,
            state.game_instance.screen.get_height() // 2 - 100
        ))
        state.game_instance.screen.blit(game_over_text, game_over_rect)
        
        mouse_pos = pygame.mouse.get_pos()
        button_color = (255, 255, 0) if self._is_button_hovered(mouse_pos) else (150, 150, 150)
        button_text = self.button_font.render("MAIN MENU", True, button_color)
        button_rect = button_text.get_rect(center=self.button_pos)
        state.game_instance.screen.blit(button_text, button_rect)

    def _is_button_hovered(self, mouse_pos: Tuple[int, int]) -> bool:
        '''Перевірка, чи наведено курсор на кнопку
        Args:
            mouse_pos (Tuple[int, int]): Позиція миші
        Return:
            bool: True, якщо курсор наведено на кнопку
        '''
        text_surf = self.button_font.render("MAIN MENU", True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=self.button_pos)
        return text_rect.collidepoint(mouse_pos)

    def handle_event(self, event: pygame.event.Event) -> str | None:
        '''Обробка подій меню завершення гри
        Args:
            event (pygame.event.Event): Подія
        Return:
            str | None: Дія, яку потрібно виконати
        '''
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self._is_button_hovered(event.pos):
                return 'GO_TO_MENU'
        return None
