import pygame
import state

class VictoryMenu:
    def __init__(self):
        self.font = pygame.font.SysFont("Arial", 80)
        self.button_font = pygame.font.SysFont("Arial", 40)
        
        screen_width = state.game_instance.screen.get_width()
        screen_height = state.game_instance.screen.get_height()
        
        button_width, button_height = 300, 80
        self.new_game_button = pygame.Rect(
            (screen_width - button_width) // 2,
            screen_height // 2,
            button_width,
            button_height
        )
        self.menu_button = pygame.Rect(
            (screen_width - button_width) // 2,
            screen_height // 2 + 120,
            button_width,
            button_height
        )
    
    def draw(self):
        state.game_instance.screen.fill((30, 30, 30))
        
        victory_text = self.font.render("VICTORY!", True, (0, 255, 0))
        victory_rect = victory_text.get_rect(center=(
            state.game_instance.screen.get_width() // 2,
            state.game_instance.screen.get_height() // 2 - 150
        ))
        state.game_instance.screen.blit(victory_text, victory_rect)
        
        mouse_pos = pygame.mouse.get_pos()
        
        # New Game Button
        new_game_color = (50, 150, 50) if self.new_game_button.collidepoint(mouse_pos) else (30, 100, 30)
        pygame.draw.rect(state.game_instance.screen, new_game_color, self.new_game_button, border_radius=10)
        new_game_text = self.button_font.render("NEW GAME", True, (255, 255, 255))
        state.game_instance.screen.blit(new_game_text, new_game_text.get_rect(center=self.new_game_button.center))
        
        # Menu Button
        menu_color = (50, 50, 150) if self.menu_button.collidepoint(mouse_pos) else (30, 30, 100)
        pygame.draw.rect(state.game_instance.screen, menu_color, self.menu_button, border_radius=10)
        menu_text = self.button_font.render("MENU", True, (255, 255, 255))
        state.game_instance.screen.blit(menu_text, menu_text.get_rect(center=self.menu_button.center))
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.new_game_button.collidepoint(event.pos):
                return 'NEW_GAME'
            if self.menu_button.collidepoint(event.pos):
                return 'GO_TO_MENU'
        return None