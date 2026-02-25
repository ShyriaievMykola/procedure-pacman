import pygame
from menus.game.config import GameMenuConfig
import state
from map.map_visualization import MapVisualization

class GameMenu:
    def __init__(self):
        self.gmc = GameMenuConfig()
        screen_width = state.game_instance.screen.get_width()
        game_map = state.game_instance.map

        # Fonts
        self.label_font = pygame.font.SysFont(self.gmc.font, self.gmc.label_font_size)
        self.input_font = pygame.font.SysFont(self.gmc.font, 32, bold=True)
        self.button_font = pygame.font.SysFont(self.gmc.font, 40, bold=True)

        # Seed input
        self.seed_text = str(state.game_instance.seed)
        self.input_rect = pygame.Rect(*self.gmc.input_seed_pos, *self.gmc.input_seed_size)
        self.active = False

        # Pre-calculate centered map offsets
        map_size = self.gmc.map_size
        cell_size = min(map_size[0] // game_map.width, map_size[1] // game_map.height)
        actual_map_width = game_map.width * cell_size
        centered_x = (screen_width - actual_map_width) // 2
        self.map_offsets = (centered_x, self.gmc.map_offsets[1])

        # Buttons
        self.buttons = [
            {'text': 'START GAME', 'pos': self.gmc.start_btn_pos, 'action': 'GET_DIFFICULTY'},
            {'text': 'BACK', 'pos': self.gmc.back_btn_pos, 'action': 'GO_BACK'}
        ]


    def draw(self):
        state.game_instance.screen.fill((0, 0, 0))
        mouse_pos = pygame.mouse.get_pos()
        
        # Label
        label = self.label_font.render("Enter Seed:", True, (200, 200, 200))
        state.game_instance.screen.blit(label, label.get_rect(center=(state.game_instance.screen.get_width() // 2, self.gmc.label_y)))
        
        # Input field
        box_color = (255, 255, 0) if self.active else (80, 80, 80)
        pygame.draw.rect(state.game_instance.screen, box_color, self.input_rect, border_radius=5)
        txt_surface = self.input_font.render(self.seed_text, True, (0, 0, 0) if self.active else (255, 255, 255))
        state.game_instance.screen.blit(txt_surface, (self.input_rect.x + 10, self.input_rect.y + 8))

        # Buttons
        for btn in self.buttons:
            color = (255, 255, 0) if self._is_button_hovered(btn, mouse_pos) else (180, 180, 180)
            text = self.button_font.render(btn['text'], True, color)
            state.game_instance.screen.blit(text, text.get_rect(center=btn['pos']))

        # Map
        MapVisualization.display_map(state.game_instance.screen, self.gmc.map_size, self.map_offsets, state.game_instance.map)

    def _is_button_hovered(self, btn, mouse_pos):
        text_surf = self.button_font.render(btn['text'], True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=btn['pos'])
        return text_rect.collidepoint(mouse_pos)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Toggle seed box focus
            self.active = True if self.input_rect.collidepoint(event.pos) else False
            
            if event.button == 1:
                for btn in self.buttons:
                    if self._is_button_hovered(btn, event.pos):
                        return btn['action']

        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.seed_text = self.seed_text[:-1]
            elif len(self.seed_text) < 12:
                if event.unicode.isalnum():
                    self.seed_text += event.unicode
        return None