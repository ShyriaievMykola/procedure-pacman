from constants import *
import keyboard 

# Будем робити по ООП, тут буде зазначений стан і позиція пекмена
position : tuple[int, int] 
movement_direction : tuple[int, int] = (0, 0) # Спочатку пекмен стоїть на місці
pending_direction : tuple[int, int] = (0, 0) # Напрямок, в який гравець хоче рухатись
                                            # (користувач вказав напрямок але поки там стіна)
points : int = 0

def get_spawn_position(maze : list # 2D Сітка лабіринту 
                    ) -> tuple[int, int]: # Повертає координати x, y
    for y, row in enumerate(maze):
        for x, cell in enumerate(row):
            if cell == EMPTY or cell == PELLET:
                return x, y

def resolve_pend(maze : list # 2D Сітка лабіринту
                ):
    global movement_direction, pending_direction, position
    new_x = position[0] + pending_direction[0]
    new_y = position[1] + pending_direction[1]
    if maze[new_y][new_x] != WALL: # Якщо можна рухатись в напрямку очікування
        movement_direction = pending_direction
        position = (new_x, new_y)
    else: # Інакше пробуємо рухатись в поточному напрямку поки не зможемо задовільнити очікування
        new_x = position[0] + movement_direction[0]
        new_y = position[1] + movement_direction[1]
        if maze[new_y][new_x] != WALL:
            position = (new_x, new_y)
        else:    # Вдарились в стіну
            pass # Стоїмо на місці
    grab(maze, position)

def grab(maze : list, # 2D Сітка лабіринту
        position : tuple[int, int]
        ) -> int: # Повертає тип тайла, який був взятий
    x, y = position
    tile = maze[y][x]
    if tile == PELLET:
        eat_pellet(maze, position)
    return tile

def eat_pellet( maze : list, # 2D Сітка лабіринту
                position : tuple[int, int] # Точка звідки їмо таблетку
                ):
    global points
    x, y = position
    maze[y][x] = EMPTY
    points += 1

def control():
    global pending_direction
    if keyboard.is_pressed('w'):
        pending_direction = (0, -1)
    elif keyboard.is_pressed('s'):
        pending_direction = (0, 1)
    elif keyboard.is_pressed('a'):
        pending_direction = (-1, 0)
    elif keyboard.is_pressed('d'):
        pending_direction = (1, 0)