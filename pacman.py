from constants import *
import pygame
from map.game_map import GameMap
import time
import keyboard
from ghosts.ghost import Ghost
from ghosts.ghost_manager import GhostManager
import visualisation.config
pygame.event.recent = []

position : tuple[int, int] 
old_position : tuple[int, int] # Позиція на попередньому кроці
movement_direction : tuple[int, int] = (0, 0) # Спочатку пекмен стоїть на місці
pending_direction : tuple[int, int] = (0, 0) # Напрямок, в який гравець хоче рухатись
                                            # (користувач вказав напрямок але поки там стіна)
points : int = 0 # Кількість очок, які набрав гравець

fruit_value : int = 1000 # Кількість очок за з'їдений фрукт

last_power_time : float = 0.0 # Час, коли пекмен останній раз з'їв power pellet
power_span : float = 10.0 # Тривалість дії підсилення в секундах
empowered : bool = False # Чи підсилений пекмен (після поїдання power pellet)
almost_lost_power : bool = False # Буде True за декілька секунд до втрати сил
almost_lost_power_span : float = 2 # Кількість часу сигналу

max_health : int = 3 # Максимальна кількість життів пекмена
health : int = max_health  # Кількість життів пекмена

invincible_span : float = 0.0 # Тривалість безсмертя після втрати життя
invincible_start_time : float = 0.0 # Час початку безсмертя після втрати життя
invincible : bool = False # Чи є пекмен безсмертним зараз
starting_points_for_ghost : int = 200
points_for_ghost : int = starting_points_for_ghost # Кількість очок за з'їденого привида
multiplier_for_ghost : float = 2.0 # Множник очок за кожного наступного з'їденого привида в одному підсиленні

def get_spawn_position(map : GameMap
                    ) -> tuple[int, int]: # Повертає координати x, y
    """Повертає координати спавну пекмена, які визначаються як перша клітинка тунелю, в якій є таблетка"""
    for y, row in enumerate(map.grid):
        for x, cell in enumerate(row):
            if cell == TUNNEL and map.pellet_grid[y][x] == PELLET:
                return x, y

def resolve_pend(map : GameMap,
                ghost_manager : GhostManager | None
                ):
    """
    Розв'язує очікуваний напрямок руху пекмена. 
    Якщо можна рухатись в напрямку очікування - рухаємось в ньому, 
    інакше пробуємо рухатись в поточному напрямку поки не зможемо задовільнити очікування, 
    інакше стоїмо на місці.
    Також з'їдає таблетку в кінці руху, якщо вона є
    """
    maze = map.grid
    global movement_direction, pending_direction, position, old_position
    old_position = position
    new_x = position[0] + pending_direction[0]
    new_y = position[1] + pending_direction[1]
    new_x = max(0, min(map.width - 1, new_x))
    new_y = max(0, min(map.height - 1, new_y))
    if maze[new_y][new_x] != WALL: # Якщо можна рухатись в напрямку очікування
        movement_direction = pending_direction
        position = (new_x, new_y)
    else: # Інакше пробуємо рухатись в поточному напрямку поки не зможемо задовільнити очікування
        new_x = position[0] + movement_direction[0]
        new_y = position[1] + movement_direction[1]
        new_x = max(0, min(map.width - 1, new_x))
        new_y = max(0, min(map.height - 1, new_y))
        if maze[new_y][new_x] != WALL:
            position = (new_x, new_y)
        else:    # Вдарились в стіну
            pass # Стоїмо на місці
    eat(position, map, ghost_manager)

def eat(position : tuple[int, int], # Точка звідки їмо таблетку
        map : GameMap,
        ghost_manager : GhostManager | None
        ):
    """
    Визначає що знаходиться в клітинці, де є пекмен, і відповідно реагує на це
    """
    x, y = position
    grid = map.pellet_grid
    if ghost_manager is not None:
        touched_ghosts = get_touched_ghost(position, ghost_manager)
        for ghost in touched_ghosts:
            touch_ghost(ghost_manager, ghost)
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

def does_touch_ghost(ghost : Ghost):
    """
    Повертає True якщо пекмен торкається привида, інакше False.
    """
    return ghost.position == position or (ghost.position == old_position and ghost.old_position == position)
    # перша частина - дотик якщо в одній клітинці
    # друга частина - дотик якщо пекмен і привид помінялись місцями за крок

def get_touched_ghost(position : tuple[int, int], # Позиція пекмена
                    ghost_manager : GhostManager # Менеджер привидів
                    ) -> list: # Повертає привидів яких пекмен торкається
    """
    Повертає список привидів, яких пекмен торкається
    """
    touching = []
    for ghost in ghost_manager.ghosts:
        if does_touch_ghost(ghost):
            touching.append(ghost)
    return touching

def any_pellets_left(map : GameMap) -> bool:
    """
    Повертає True якщо на карті залишились таблетки, інакше False.
    """
    for y in range(map.height):
        for x in range(map.width):
            if map.pellet_grid[y][x] == PELLET and map.grid[y][x] != WALL:  
                # Поїдання усилення не обов'язкове 
                # для перемоги в стандартному пекмені
                return True
    return False

def go_through_passage_left(map : GameMap):
    """
    Переміщує пекмена через ліву телепортаційну трубу на праву
    """
    global position
    position = map.passage_right

def go_through_passage_right(map : GameMap):
    """
    Переміщує пекмена через праву телепортаційну трубу на ліву
    """
    global position
    position = map.passage_left

def eat_pellet( map : GameMap,
                position : tuple[int, int] # Точка звідки їмо таблетку
                ):
    """
    З'їдає таблетку в даній клітинці, додає очки, і перевіряє чи не переміг гравець після цього
    """
    global points
    empty_cell(map, position)
    points += 1
    if any_pellets_left(map) == False:
        victory() # Перемога, всі таблетки з'їдені

def eat_fruit( map : GameMap,
                position : tuple[int, int] # Точка звідки їмо таблетку
                ):
    """
    З'їдає фрукт в даній клітинці і додає очки
    """
    global points
    empty_cell(map, position)
    points += fruit_value

def eat_power_pellet(map : GameMap,
                    position : tuple[int, int] # Точка звідки їмо таблетку
                    ):
    """
    З'їдає підсилення в даній клітинці, додає очки, і робить пекмена підсиленим на деякий час
    """
    global empowered, last_power_time
    empty_cell(map, position)
    last_power_time = time.time()
    empowered = True

def touch_ghost(ghost_manager : GhostManager, ghost : Ghost):
    """
    Опрацьовує логіку дотику пекмена до привида. 
    Якщо пекмен підсилений і привид наляканий - з'їдаємо привида, 
    інакше якщо пекмен не безсмертний і привид не з'їдений - втрачаємо життя, 
    робимо пекмена безсмертним на деякий час, і якщо життя закінчились - програємо
    """
    global health, invincible, invincible_start_time
    if empowered and ghost.is_frightened():
        eat_ghost(ghost_manager, ghost)
    elif not invincible and not ghost.is_eaten():
        health -= 1
        if health <= 0:
            game_over()
        invincible = True
        invincible_start_time = time.time()

def game_over():
    """
    Опрацьовує логіку програшу гравця. Відображає екран програшу і чекає на дію гравця
    """
    visualisation.config.state = visualisation.config.play_state.GAME_OVER

def victory():
    """
    Вітаю! ви перемогли! Опрацьовує логіку перемоги гравця. Відображає екран перемоги і чекає на дію гравця
    """
    visualisation.config.state = visualisation.config.play_state.VICTORY

def eat_ghost(ghost_manager : GhostManager, ghost : Ghost):
    """
    З'їдає привида, додає очки, і відображає повідомлення про з'їдання привида
    З кожним наступним з'їденим привидом в одному підсиленні кількість очок за нього збільшується в кілька разів
    """
    global points, points_for_ghost
    points += points_for_ghost
    print(f"Ate ghost for {points_for_ghost} points!")
    ghost_manager.be_eaten(ghost)
    points_for_ghost = points_for_ghost * multiplier_for_ghost

def empty_cell( map : GameMap,
                position : tuple[int, int] # Точка звідки їмо таблетку
                ):
    """
    Змінює клітинку на порожню після поїдання таблетки або фрукта
    """
    grid = map.pellet_grid
    x, y = position
    grid[y][x] = EMPTY

def control():
    """
    Визначає напрямок руху пекмена на основі натиснутих клавіш. Зберігає його в pending_direction,
    щоб resolve_pend міг його розв'язати і застосувати.
    """
    global pending_direction
    for event in pygame.event.recent:
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_w, pygame.K_UP):
                pending_direction = (0, -1)
            elif event.key in (pygame.K_s, pygame.K_DOWN):
                pending_direction = (0, 1)
            elif event.key in (pygame.K_a, pygame.K_LEFT):
                pending_direction = (-1, 0)
            elif event.key in (pygame.K_d, pygame.K_RIGHT):
                pending_direction = (1, 0)

def old_control():
    """
    Стара версія control, яка використовує бібліотеку keyboard замість pygame для визначення натиснутих клавіш.
    Потрібна для роботи в консолі, де немає доступу до подій pygame.
    """
    global pending_direction
    if keyboard.is_pressed('w') or keyboard.is_pressed('up'):
        pending_direction = (0, -1)
    elif keyboard.is_pressed('s') or keyboard.is_pressed('down'):
        pending_direction = (0, 1)
    elif keyboard.is_pressed('a') or keyboard.is_pressed('left'):
        pending_direction = (-1, 0)
    elif keyboard.is_pressed('d') or keyboard.is_pressed('right'):
        pending_direction = (1, 0)

def maybe_lose_power():
    """
    Перевіряє чи не закінчився час підсилення, і якщо так - вимикає його 
    і скидає кількість очок за привида до початкового значення
    """
    global empowered, almost_lost_power, points_for_ghost
    if time.time() - last_power_time > power_span - almost_lost_power_span:
        almost_lost_power = True
    if time.time() - last_power_time > power_span:
        empowered = False
        points_for_ghost = starting_points_for_ghost
        almost_lost_power = False

def maybe_lose_invincibility():
    """
    Перевіряє чи не закінчився час безсмертя, і якщо так - вимикає його
    """
    global invincible
    if time.time() - invincible_start_time > invincible_span:
        invincible = False

def update( map : GameMap,
            ghost_manager : GhostManager | None
            ):
    """
    Цю функцію треба викликати кожного кроку, щоб оновити стан гри
    """
    control()
    resolve_pend(map, ghost_manager)
    if empowered:
        maybe_lose_power()
    if invincible:
        maybe_lose_invincibility()

def old_update( map : GameMap,
                ghost_manager : GhostManager | None
                ):
    """
    Старе оновлення, яке використовує old_control замість control для роботи в консолі
    """
    old_control()
    resolve_pend(map, ghost_manager)
    if empowered:
        maybe_lose_power()
    if invincible:
        maybe_lose_invincibility()