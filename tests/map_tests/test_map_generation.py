import pytest

from constants import EMPTY, FRUIT, PELLET, POWER, TUNNEL, WALL
from map.config import MapGeneratorConfig as cfg
from map.game_map import GameMap
from map.map_generator import MapGenerator
from seeded_random import SeededRandom


pytestmark = [pytest.mark.map, pytest.mark.map_generation]


@pytest.fixture
def generated_map():
    return MapGenerator.generate_map(width=21, height=21, seed=1234)
    

def test_generate_map_returns_gamemap_with_expected_dimensions(generated_map):
    assert isinstance(generated_map, GameMap)
    assert generated_map.width == 21
    assert generated_map.height == 21
    assert generated_map.seed == 1234
    assert len(generated_map.grid) == 21
    assert len(generated_map.grid[0]) == 21
    assert len(generated_map.pellet_grid) == 21
    assert len(generated_map.pellet_grid[0]) == 21


def test_ghost_room_cells_are_tunnels(generated_map):
    for y in range(generated_map.ghost_y[0], generated_map.ghost_y[1] + 1):
        for x in range(generated_map.ghost_x[0], generated_map.ghost_x[1] + 1):
            assert generated_map.grid[y][x] == TUNNEL


def test_side_passages_are_open_in_middle_row(generated_map):
    middle_y = generated_map.height // 2

    assert generated_map.passage_left == (0, middle_y)
    assert generated_map.passage_right == (generated_map.width - 1, middle_y)

    for x in range(3):
        assert generated_map.grid[middle_y][x] == TUNNEL
        assert generated_map.grid[middle_y][generated_map.width - 1 - x] == TUNNEL


def test_spawn_fruit_places_fruit_below_ghost_room(generated_map):
    fruit_x = (generated_map.ghost_x[0] + generated_map.ghost_x[1]) // 2
    fruit_y = generated_map.ghost_y[1] + 2

    assert generated_map.pellet_grid[fruit_y][fruit_x] == FRUIT


def test_pellets_not_spawned_in_ghost_room(generated_map):
    for y in range(generated_map.ghost_y[0], generated_map.ghost_y[1] + 1):
        for x in range(generated_map.ghost_x[0], generated_map.ghost_x[1] + 1):
            assert generated_map.pellet_grid[y][x] == EMPTY


def test_power_pellet_count_matches_config(generated_map):
    expected_count = int((generated_map.height * generated_map.width * cfg.POWER_COVERAGE / 100) // 1)
    actual_count = sum(
        1
        for row in generated_map.pellet_grid
        for cell in row
        if cell == POWER
    )

    assert actual_count == expected_count


def test_generate_map_is_deterministic_for_same_seed_when_power_choice_is_fixed():
    map_a = MapGenerator.generate_map(width=21, height=21, seed=777)
    map_b = MapGenerator.generate_map(width=21, height=21, seed=777)

    assert map_a.grid == map_b.grid
    assert map_a.pellet_grid == map_b.pellet_grid


@pytest.mark.pathfinding
def test_path_exists_returns_true_for_connected_tunnels():
    grid = [
        [WALL, WALL, WALL, WALL, WALL],
        [WALL, TUNNEL, TUNNEL, TUNNEL, WALL],
        [WALL, WALL, WALL, TUNNEL, WALL],
        [WALL, TUNNEL, TUNNEL, TUNNEL, WALL],
        [WALL, WALL, WALL, WALL, WALL],
    ]

    assert MapGenerator.path_exists(grid, (1, 1), (3, 3)) is True


@pytest.mark.pathfinding
def test_path_exists_returns_false_when_target_is_blocked():
    grid = [
        [WALL, WALL, WALL],
        [WALL, TUNNEL, WALL],
        [WALL, WALL, WALL],
    ]

    assert MapGenerator.path_exists(grid, (1, 1), (2, 1)) is False


@pytest.mark.pellets
def test_clear_pellet_grid_resets_all_cells_to_empty():
    game_map = GameMap(
        width=3,
        height=3,
        pellet_grid=[
            [PELLET, POWER, FRUIT],
            [EMPTY, PELLET, POWER],
            [FRUIT, EMPTY, PELLET],
        ],
    )

    MapGenerator.clear_pellet_grid(game_map)

    assert game_map.pellet_grid == [[EMPTY, EMPTY, EMPTY] for _ in range(3)]


@pytest.mark.pellets
def test_spawn_pellets_places_only_on_tunnels_and_never_in_ghost_room():
    game_map = GameMap(width=7, height=7)
    game_map.grid = [[WALL for _ in range(7)] for _ in range(7)]
    game_map.pellet_grid = [[EMPTY for _ in range(7)] for _ in range(7)]
    game_map.untouchable_zones = [[False for _ in range(7)] for _ in range(7)]

    for i in range(1, 6):
        game_map.grid[3][i] = TUNNEL
        game_map.grid[i][3] = TUNNEL

    game_map.ghost_x = (2, 4)
    game_map.ghost_y = (2, 4)

    MapGenerator.spawn_pellets(game_map, SeededRandom(1))

    for y in range(game_map.height):
        for x in range(game_map.width):
            in_ghost_room = game_map.ghost_x[0] <= x <= game_map.ghost_x[1] and game_map.ghost_y[0] <= y <= game_map.ghost_y[1]
            if in_ghost_room:
                assert game_map.pellet_grid[y][x] == EMPTY
            elif game_map.grid[y][x] == TUNNEL and 0 < x < 6 and 0 < y < 6:
                assert game_map.pellet_grid[y][x] in (EMPTY, PELLET)
            else:
                assert game_map.pellet_grid[y][x] == EMPTY
