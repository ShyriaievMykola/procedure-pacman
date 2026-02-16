import pygame
from menus.game.config import GameMenuConfig
import state
from map.map_visualization import MapVisualization

class GameMenu:
    def __init__(self):
        self.gmc = GameMenuConfig()

        self.font = pygame.font.SysFont(self.gmc.font, self.gmc.font_size)

        self.seed_text = str(state.game_instance.seed)
        self.input_rect = pygame.Rect(*self.gmc.input_seed_pos, *self.gmc.input_seed_size)
        self.active = False

        self.buttons = [
            {
                'text': 'START GAME',
                'rect': pygame.Rect(*self.gmc.start_btn_pos, *self.gmc.button_size),
                'action': 'START_GAME'
            },
            {
                'text': 'BACK',
                'rect': pygame.Rect(*self.gmc.back_btn_pos, *self.gmc.button_size),
                'action': 'GO_BACK'
            }
        ]


    def draw(self):
        state.game_instance.screen.fill(self.gmc.backg_color)
        mouse_pos = pygame.mouse.get_pos()
        
        label = self.font.render("Enter Seed:", True, (self.gmc.seed_input_text_color))
        state.game_instance.screen.blit(label, (300, 300))
        
        box_color = (255, 255, 255) if self.active else (180, 180, 180)
        pygame.draw.rect(state.game_instance.screen, box_color, self.input_rect, border_radius=5)
        
        txt_surface = self.font.render(self.seed_text, True, (0, 0, 0))
        state.game_instance.screen.blit(txt_surface, (self.input_rect.x + 10, self.input_rect.y + 5))

        # Draw Buttons
        for btn in self.buttons:
            color = (200, 100, 200) if btn['rect'].collidepoint(mouse_pos) else (150, 50, 150)
            pygame.draw.rect(state.game_instance.screen, color, btn['rect'], border_radius=10)
            text_surf = self.font.render(btn['text'], True, (255, 255, 255))
            state.game_instance.screen.blit(text_surf, text_surf.get_rect(center=btn['rect'].center))

        MapVisualization.display_map(state.game_instance.screen, self.gmc.map_size, self.gmc.map_offsets, state.game_instance.map)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Toggle seed box focus
            self.active = True if self.input_rect.collidepoint(event.pos) else False
            
            if event.button == 1:
                for btn in self.buttons:
                    if btn['rect'].collidepoint(event.pos):
                        return btn['action']

        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.seed_text = self.seed_text[:-1]
            elif len(self.seed_text) < 12:
                if event.unicode.isalnum():
                    self.seed_text += event.unicode
        return None