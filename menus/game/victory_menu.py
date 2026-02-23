import pygame
import state

class VictoryMenu:
    def __init__(self):
        self.font = pygame.font.SysFont("Arial", 80)
        self.button_font = pygame.font.SysFont("Arial", 50, bold=True)
        
        screen_width = state.game_instance.screen.get_width()
        screen_height = state.game_instance.screen.get_height()
        
        self.new_game_pos = (screen_width // 2, screen_height // 2)
        self.menu_pos = (screen_width // 2, screen_height // 2 + 80)
    
    def draw(self):
        state.game_instance.screen.fill((0, 0, 0))
        
        victory_text = self.font.render("VICTORY!", True, (100, 255, 100))
        victory_rect = victory_text.get_rect(center=(
            state.game_instance.screen.get_width() // 2,
            state.game_instance.screen.get_height() // 2 - 150
        ))
        state.game_instance.screen.blit(victory_text, victory_rect)
        
        mouse_pos = pygame.mouse.get_pos()
        
        # New Game Button
        new_game_color = (255, 255, 0) if self._is_button_hovered('NEW GAME', self.new_game_pos, mouse_pos) else (150, 150, 150)
        new_game_text = self.button_font.render("NEW GAME", True, new_game_color)
        new_game_rect = new_game_text.get_rect(center=self.new_game_pos)
        state.game_instance.screen.blit(new_game_text, new_game_rect)
        
        # Menu Button
        menu_color = (255, 255, 0) if self._is_button_hovered("MENU", self.menu_pos, mouse_pos) else (150, 150, 150)
        menu_text = self.button_font.render("MENU", True, menu_color)
        menu_rect = menu_text.get_rect(center=self.menu_pos)
        state.game_instance.screen.blit(menu_text, menu_rect)
    
    def _is_button_hovered(self, text, pos, mouse_pos):
        text_surf = self.button_font.render(text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=pos)
        return text_rect.collidepoint(mouse_pos)
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self._is_button_hovered('NEW GAME', self.new_game_pos, event.pos):
                return 'NEW_GAME'
            if self._is_button_hovered("MENU", self.menu_pos, event.pos):
                return 'GO_TO_MENU'
        return None