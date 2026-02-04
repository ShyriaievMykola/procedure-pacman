class CameraConfig:
    ACCELERATION = 0.5
    FRICTION = 0.85
    MIN_VELOCITY = 0.1
    SPEED_DIVISOR = 3

class GraphicsConfig:
    DOT_SIZE_DIVISOR = 10
    MIN_DOT_SIZE = 2
    POWER_PELLET_SIZE_DIVISOR = 4
    MIN_POWER_PELLET_SIZE = 5
    WALL_BORDER_WIDTH = 2
    TEXT_FONT_SIZE = 48
    TEXT_MARGIN = 30

class GameConfig:
    PACMAN_SPEED_MS = 190       # Швидкість кроку по сітці
    CAMERA_SMOOTHING = 0.1      # Плавність камери
    MOUTH_ANIM_SPEED = 120      # Швидкість анімації рота
    PACMAN_RADIUS_OFFSET = 3    # Відступ від стінок