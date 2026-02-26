import state, pygame

class MainMenuConfig():
    """
    Конфігурація головного меню гри
    Attributes:
        button_size (tuple): Розмір кнопок
        begin_btn_pos (tuple): Позиція кнопки "Почати гру"
        quit_btn_pos (tuple): Позиція кнопки "Вихід"
        font (str): Назва шрифту для відображення тексту
        font_size (int): Розмір шрифту для відображення тексту
    """
    def __init__(self):

        # default values
        screen_height = pygame.display.get_surface().get_height()
        screen_width = pygame.display.get_surface().get_width()
        
        self.button_size = (220, 60)

        # Center buttons horizontally
        button_x = (screen_width - self.button_size[0]) // 2
        self.begin_btn_pos = (button_x, 380)
        self.quit_btn_pos = (button_x, 480)

        self.font = "Arial"
        self.font_size = 40

class DifficultyConfig():
    """
    Конфігурація меню складності гри
    Attributes:
        button_size (tuple): Розмір кнопок
        font (str): Назва шрифту для відображення тексту
        easy_btn_pos (tuple): Позиція кнопки "Легко"
        medium_btn_pos (tuple): Позиція кнопки "Середньо"
        hard_btn_pos (tuple): Позиція кнопки "Складно"
        back_btn_pos (tuple): Позиція кнопки "Назад"
        font (str): Назва шрифту для відображення тексту
        font_size (int): Розмір шрифту для відображення тексту
    """
    def __init__(self):

        screen_height = pygame.display.get_surface().get_height()
        screen_width = pygame.display.get_surface().get_width()

        self.button_size = (220, 60)

        button_x = (screen_width - self.button_size[0]) // 2
        self.easy_btn_pos   = (screen_width // 2, 340)
        self.medium_btn_pos = (screen_width // 2, 420)
        self.hard_btn_pos   = (screen_width // 2, 500)
        self.back_btn_pos   = (screen_width // 2, 580)

        self.font       = "Arial"
        self.font_size  = 40