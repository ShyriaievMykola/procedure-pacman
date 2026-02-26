import pygame
import sys
from menus.main.choose_difficulty import DifficultyMenu
from menus.main.main_menu import MainMenu
from menus.game.game_menu import GameMenu
from menus.game.game_over_menu import GameOverMenu
from menus.game.victory_menu import VictoryMenu
import random
import state
from map.map_generator import MapGenerator
from visualisation.pacman_visualizer import PacManVisualizer
from visualisation.visualizer import Visualizer
from difficulty_manager import DifficultyManager
from visualisation.config import DifficultyConfig
import pacman


class GameManager:
    """
    Клас-оркестратор гри
    """
    def __init__(self):
        state.game_instance = self
        self.generated = False
        # Ініціалізація меню
        pygame.init()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption("Game with Seed System")
        self.clock = pygame.time.Clock()
        self.running = True

        # Змінні гри
        self.seed = random.randint(0, 10000)
        self.map_size = (21, 36)
        self.map = MapGenerator.generate_map(*self.map_size, self.seed)
        
        # Debounce
        self.last_input_time = 0
        self.debounce_delay = 300
        self.needs_regeneration = False

        
        self.state = 'MENU'

        self.main_menu = MainMenu()
        self.seed_menu = GameMenu()
        self.game_over_menu = GameOverMenu()
        self.victory_menu = VictoryMenu()

        self.dif_config = DifficultyConfig()
        self.dif_manager = DifficultyManager(self.dif_config)
        self.dif_menu = DifficultyMenu()
        self.dif_manager.set_hard()



    def run(self):
        """
        Запуск циклу життя гри
        """
        while self.running:
            self._handle_events()
            self._update()
            self._draw()
            self.clock.tick(60)
        pygame.quit()
        sys.exit()

    def _handle_events(self):
        """
        Оброка подій гри
        """
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
                if not self.generated:
                    self._generate_new_map()
                    self.generated = True
                if event.type == pygame.KEYDOWN and self.seed_menu.active:
                    self.last_input_time = pygame.time.get_ticks()
                    self.needs_regeneration = True

                if action == 'GET_DIFFICULTY':
                    self.state = 'DIFFICULTY'
                elif action == 'GO_BACK':
                    self.state = 'MENU'
            else:
                self.generated = False

            if self.state == 'DIFFICULTY':
                action = self.dif_menu.handle_event(event)
                if action == 'SET_EASY':
                    self.dif_manager.set_difficulty(1)
                    print("Difficulty set to EASY")
                    self.state = 'GAME'
                elif action == 'SET_MEDIUM':
                    self.dif_manager.set_difficulty(2)
                    print("Difficulty set to MEDIUM")
                    self.state = 'GAME'
                elif action == 'SET_HARD':
                    self.dif_manager.set_difficulty(3)
                    print("Difficulty set to HARD")
                    self.state = 'GAME'

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
        """
        Обробка оновлень гри
        """
        if self.state == 'SEED_INPUT' and self.needs_regeneration:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_input_time > self.debounce_delay:
                self._generate_new_map()
                self.needs_regeneration = False

    def _generate_new_map(self):
        """
        Перегенерація карти
        """
        raw_text = self.seed_menu.seed_text
        if not raw_text:
            new_seed = 0
        else:
            new_seed = int(raw_text) if raw_text.isdigit() else hash(raw_text)
        
        self.seed = new_seed
        self.map = MapGenerator.generate_map(*self.map_size, self.seed)
        
        pacman.health = pacman.max_health
        pacman.points = 0
        pacman.empowered = False
        pacman.invincible = False

    def _draw(self):
        """
        Промальовка меню
        """
        if self.state == 'MENU':
            self.main_menu.draw()
        elif self.state == 'SEED_INPUT':
            self.seed_menu.draw()
        elif self.state == 'DIFFICULTY':
            self.dif_menu.draw()
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

