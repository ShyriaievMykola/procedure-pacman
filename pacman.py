from constants import *
import keyboard 
from map.game_map import GameMap
import time

# Будем робити по ООП, тут буде зазначений стан і позиція пекмена
position : tuple[int, int] 
movement_direction : tuple[int, int] = (0, 0) # Спочатку пекмен стоїть на місці
pending_direction : tuple[int, int] = (0, 0) # Напрямок, в який гравець хоче рухатись
                                            # (користувач вказав напрямок але поки там стіна)
points : int = 0

fruit_value : int = 100 # Кількість очок за з'їдений фрукт

last_power_time : float = 0.0 # Час, коли пекмен останній раз з'їв power pellet
power_span : float = 10.0 # Тривалість дії підсилення в секундах
empowered : bool = False # Чи підсилений пекмен (після поїдання power pellet)

health : int = 3 # Кількість життів пекмена
invincible_span : float = 3.0 # Тривалість безсмертя після втрати життя
invincible_start_time : float = 0.0 # Час початку безсмертя після втрати життя
invincible : bool = False # Чи є пекмен безсмертним зараз
points_for_ghost : int = 200 # Кількість очок за з'їденого привида

def get_spawn_position(map : GameMap
                    ) -> tuple[int, int]: # Повертає координати x, y
    
    for y, row in enumerate(map.grid):
        for x, cell in enumerate(row):
            if cell == TUNNEL:
                return x, y

def resolve_pend(map : GameMap
                ):
    maze = map.grid
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
    eat(position, map)

def eat(position : tuple[int, int], # Точка звідки їмо таблетку
        map : GameMap
        ):
    x, y = position
    grid = map.grid
    if (x,y) == map.passage_left:
        go_through_passage_left(map)
    elif (x,y) == map.passage_right:
        go_through_passage_right(map)
    elif grid[y][x] == PELLET:
        eat_pellet(map, position)
    elif grid[y][x] == POWER:
        eat_power_pellet(map, position)
    elif grid[y][x] == FRUIT:
        eat_fruit(map, position)
    # Сюди додати поїдання таблеток, бонусів і т.д.


def go_through_passage_left(map : GameMap):
    global position
    position = map.passage_right

def go_through_passage_right(map : GameMap):
    global position
    position = map.passage_left

def eat_pellet( map : GameMap,
                position : tuple[int, int] # Точка звідки їмо таблетку
                ):
    global points
    empty_cell(map, position)
    points += 1

def eat_fruit( map : GameMap,
                position : tuple[int, int] # Точка звідки їмо таблетку
                ):
    global points
    empty_cell(map, position)
    points += fruit_value

def eat_power_pellet(map : GameMap,
                    position : tuple[int, int] # Точка звідки їмо таблетку
                    ):
    global empowered, last_power_time
    empty_cell(map, position)
    empowered = True
    last_power_time = time.time()

def touch_ghost():
    global health, invincible, invincible_start_time
    if empowered:
        eat_ghost()
    elif not invincible:
        health -= 1
        invincible = True
        invincible_start_time = time.time()

def eat_ghost():
    global points
    points += points_for_ghost
    raise NotImplementedError("Функція eat_ghost ще не реалізована")

def empty_cell( map : GameMap,
                position : tuple[int, int] # Точка звідки їмо таблетку
                ):
    pass # Згодом коли пойму логіку то додам

def control(): # Слід змінити під pygame
    global pending_direction
    if keyboard.is_pressed('w'):
        pending_direction = (0, -1)
    elif keyboard.is_pressed('s'):
        pending_direction = (0, 1)
    elif keyboard.is_pressed('a'):
        pending_direction = (-1, 0)
    elif keyboard.is_pressed('d'):
        pending_direction = (1, 0)

def maybe_lose_power():
    global empowered
    if time.time() - last_power_time > power_span:
        empowered = False

def maybe_lose_invincibility():
    global invincible
    if time.time() - invincible_start_time > invincible_span:
        invincible = False

def update(map : GameMap):
    control()
    resolve_pend(map)
    if empowered:
        maybe_lose_power()
    if invincible:
        maybe_lose_invincibility()