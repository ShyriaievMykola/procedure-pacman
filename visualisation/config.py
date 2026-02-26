from enum import Enum


class CameraConfig:
    """
    Клас конфігурацій для управління поведінкою камери у грі.
    Визначає параметри прискорення, тертя та розділювачі швидкості.
    """
    ACCELERATION = 0.5
    FRICTION = 0.85
    MIN_VELOCITY = 0.1
    SPEED_DIVISOR = 3

class GraphicsConfig:
    """
    Клас конфігурацій для графічних параметрів гри.
    Містить значення розмірів пелетів, ширини обводок та розміри текстового шрифту.
    """
    # Пелети
    DOT_SIZE_DIVISOR = 10
    MIN_DOT_SIZE = 2
    POWER_PELLET_SIZE_DIVISOR = 4
    MIN_POWER_PELLET_SIZE = 5
    
    # Стіни
    WALL_BORDER_WIDTH = 5
    
    # Текст
    TEXT_FONT_SIZE = 48
    TEXT_MARGIN = 30


class GameConfig:
    """
    Клас конфігурацій для основних параметрів гри.
    Містить налаштування для Pac-Man, камери, привидів та їхніх анімацій.
    """
    # Pac-Man
    PACMAN_RADIUS_OFFSET = 3    # Відступ від стінок
    MOUTH_ANIM_SPEED = 120      # Швидкість анімації рота
    
    # Камера
    CAMERA_SMOOTHING = 0.1      # Плавність камери
    
    # Привиди
    GHOST_EYE_OFFSET_X_DIVISOR = 3      # Відступ очей по X (radius // 3)
    GHOST_EYE_OFFSET_Y_DIVISOR = 4      # Відступ очей по Y (radius // 4)
    GHOST_EYE_RADIUS_DIVISOR = 4        # Радіус ока (radius // 4)
    GHOST_PUPIL_RADIUS_DIVISOR = 2      # Радіус зіниці (eye_radius // 2)
    GHOST_PUPIL_MOVE_DIVISOR = 3        # Рух зіниці (eye_radius // 3)
    GHOST_WAVE_COUNT = 3                # Кількість хвиль на ніжках
    GHOST_WAVE_HEIGHT_DIVISOR = 3       # Висота хвилі (wave_width // 3)
    GHOST_FRIGHTENED_BLINK_SPEED = 200  # Швидкість миготіння (мс)


class DifficultyConfig:
    """
    Клас конфігурацій для параметрів складності гри.
    Визначає швидкість руху Pac-Man та привидів у мілісекундах.
    """
    GHOST_SPEED_MS = 190                # Швидкість кроку привидів
    PACMAN_SPEED_MS = 190       # Швидкість кроку по сітці

class play_state(Enum):
    PLAYING = 1
    GAME_OVER = 2
    VICTORY = 3

state = play_state.PLAYING