import pygame
import sys
from menus.main.main_menu import MainMenu
from menus.game.game_menu import GameMenu
from menus.game.game_over_menu import GameOverMenu
from menus.game.victory_menu import VictoryMenu
import random
import state
from map.map_generator import MapGenerator
import game_config as config
from visualisation.pacman_visualizer import PacManVisualizer
from visualisation.visualizer import Visualizer

class GameManager:
    def __init__(self):
        state.game_instance = self
        
        # Ініціалізація меню
        pygame.init()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption("Game with Seed System")
        self.clock = pygame.time.Clock()
        self.running = True

        # Змінні гри
        self.seed = random.randint(0, 10000)
        self.map = MapGenerator.generate_map(*config.map_size, self.seed)
        
        # Debounce
        self.last_input_time = 0
        self.debounce_delay = 300
        self.needs_regeneration = False

        
        self.state = 'MENU'

        self.main_menu = MainMenu()
        self.seed_menu = GameMenu()
        self.game_over_menu = GameOverMenu()
        self.victory_menu = VictoryMenu()



    def run(self):
        while self.running:
            self._handle_events()
            self._update()
            self._draw()
            self.clock.tick(60)
        pygame.quit()
        sys.exit()

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if self.state == 'MENU':
                action = self.main_menu.handle_event(event)
                if action == 'GO_TO_SEED':
                    self.state = 'SEED_INPUT'
                elif action == 'QUIT':
                    self.running = False
            
            elif self.state == 'SEED_INPUT':
                action = self.seed_menu.handle_event(event)
                
                if event.type == pygame.KEYDOWN and self.seed_menu.active:
                    self.last_input_time = pygame.time.get_ticks()
                    self.needs_regeneration = True

                if action == 'START_GAME':
                    self._generate_new_map()
                    self.state = 'GAME'
                elif action == 'GO_BACK':
                    self.state = 'MENU'

            elif self.state == 'GAME':
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.state = 'MENU'

            elif self.state == 'GAME_OVER':
                action = self.game_over_menu.handle_event(event)
                if action == 'GO_TO_MENU':
                    self.state = 'MENU'

            elif self.state == 'VICTORY':
                action = self.victory_menu.handle_event(event)
                if action == 'NEW_GAME':
                    self._generate_new_map()
                    self.state = 'GAME'
                elif action == 'GO_TO_MENU':
                    self.state = 'MENU'

    def _update(self):
        if self.state == 'SEED_INPUT' and self.needs_regeneration:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_input_time > self.debounce_delay:
                self._generate_new_map()
                self.needs_regeneration = False

    def _generate_new_map(self):
        raw_text = self.seed_menu.seed_text
        if not raw_text:
            new_seed = 0
        else:
            new_seed = int(raw_text) if raw_text.isdigit() else hash(raw_text)
        
        self.seed = new_seed
        self.map = MapGenerator.generate_map(*config.map_size, self.seed)
        
        import pacman
        pacman.health = 3
        pacman.points = 0
        pacman.empowered = False
        pacman.invincible = False

    def _draw(self):
        if self.state == 'MENU':
            self.main_menu.draw()
        elif self.state == 'SEED_INPUT':
            self.seed_menu.draw()
        elif self.state == 'GAME':
            game = PacManVisualizer(self.screen, self.map)
            result = game.run()
            if result == 'GAME_OVER':
                self.state = 'GAME_OVER'
            elif result == 'VICTORY':  # Додаємо перевірку на перемогу
                self.state = 'VICTORY'
            else:
                self.state = 'MENU'
        elif self.state == 'GAME_OVER':
            self.game_over_menu.draw()
        elif self.state == 'VICTORY':  # Додаємо відображення Victory Menu
            self.victory_menu.draw()
            
        pygame.display.flip()

