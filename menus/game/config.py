import state, pygame

class GameMenuConfig():
    def __init__(self):

        # default values
        screen_width = pygame.display.get_surface().get_width()
        screen_height = pygame.display.get_surface().get_height()

        self.button_size = (220, 60)
        self.input_seed_size = (300, 50)

        # Center positioning - map on top
        self.map_size = (350, 350)
        self.map_offsets = ((screen_width - 350) // 2, 40)

        # Input field centered, below map with proper spacing
        input_x = (screen_width - self.input_seed_size[0]) // 2
        self.input_seed_pos = (input_x, 420)
        self.label_y = 400

        # Buttons centered horizontally with more spacing
        self.start_btn_pos = (screen_width // 2, 530)
        self.back_btn_pos = (screen_width // 2, 620)

        self.backg_color = (0, 0, 0)
        self.seed_input_text_color = (255, 255, 255)

        self.font = "Arial"
        self.font_size = 40
        self.label_font_size = 28