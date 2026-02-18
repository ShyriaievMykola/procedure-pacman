import pygame
import state

class GameOverMenu:
    def __init__(self):
        self.font = pygame.font.SysFont("Arial", 80)
        self.button_font = pygame.font.SysFont("Arial", 40)
        
        screen_width = state.game_instance.screen.get_width()
        screen_height = state.game_instance.screen.get_height()
        
        button_width, button_height = 300, 80
        self.button_rect = pygame.Rect(
            (screen_width - button_width) // 2,
            screen_height // 2 + 100,
            button_width,
            button_height
        )
    
    def draw(self):
        state.game_instance.screen.fill((30, 30, 30))
        
        game_over_text = self.font.render("GAME OVER", True, (255, 0, 0))
        game_over_rect = game_over_text.get_rect(center=(
            state.game_instance.screen.get_width() // 2,
            state.game_instance.screen.get_height() // 2 - 100
        ))
        state.game_instance.screen.blit(game_over_text, game_over_rect)
        
        mouse_pos = pygame.mouse.get_pos()
        button_color = (150, 50, 50) if self.button_rect.collidepoint(mouse_pos) else (100, 30, 30)
        pygame.draw.rect(state.game_instance.screen, button_color, self.button_rect, border_radius=10)
        
        button_text = self.button_font.render("MAIN MENU", True, (255, 255, 255))
        state.game_instance.screen.blit(button_text, button_text.get_rect(center=self.button_rect.center))
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.button_rect.collidepoint(event.pos):
                return 'GO_TO_MENU'
        return None
