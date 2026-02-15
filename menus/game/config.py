import state, pygame

class GameMenuConfig():
    def __init__(self):

        # default values
        screen_width = pygame.display.get_surface().get_width()
        screen_height = pygame.display.get_surface().get_width()

        self.button_size = (200, 60)
        self.input_seed_size = (250, 50)

        self.button_start_x = (screen_width - self.button_size[0]) // 4
        self.map_size = (500, 500)
        self.map_offsets = (500, 500)

        self.start_btn_pos = (300, 450)
        self.back_btn_pos = (50, 50)
        self.input_seed_pos = (300, 350)

        self.backg_color = (200, 200, 200)
        self.seed_input_text_color = (100, 100, 100)

        self.font = "Arial"
        self.font_size = 40