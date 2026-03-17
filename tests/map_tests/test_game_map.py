import pytest

from constants import EMPTY, PELLET, WALL
from map.game_map import GameMap


pytestmark = [pytest.mark.map, pytest.mark.game_map]


def make_map(grid, pellet_grid=None):
    height = len(grid)
    width = len(grid[0])
    if pellet_grid is None:
        pellet_grid = [[EMPTY for _ in range(width)] for _ in range(height)]

    return GameMap(
        height=height,
        width=width,
        grid=grid,
        pellet_grid=pellet_grid,
        ghost_x=(1, 1),
        ghost_y=(1, 1),
        ghost_door=(1, 0),
        passage_left=(0, height // 2),
        passage_right=(width - 1, height // 2),
    )


def test_get_texture_map_returns_minus_one_for_tunnel_cells():
    game_map = make_map(
        [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]
    )

    texture = game_map.get_texture_map()

    assert texture == [[-1, -1, -1], [-1, -1, -1], [-1, -1, -1]]


def test_get_texture_map_mask_for_isolated_wall_is_zero():
    game_map = make_map(
        [
            [0, 0, 0],
            [0, WALL, 0],
            [0, 0, 0],
        ]
    )

    texture = game_map.get_texture_map()

    assert texture[1][1] == 0


def test_get_texture_map_mask_for_cross_neighbors_is_fifteen():
    game_map = make_map(
        [
            [0, WALL, 0],
            [WALL, WALL, WALL],
            [0, WALL, 0],
        ]
    )

    texture = game_map.get_texture_map()

    assert texture[1][1] == 15


def test_get_texture_map_handles_edge_cells_correctly():
    game_map = make_map(
        [
            [WALL, WALL, 0],
            [WALL, 0, 0],
            [0, 0, 0],
        ]
    )

    texture = game_map.get_texture_map()

    # Для клітинки (0,0): право = 2, низ = 4, сумарно 6.
    assert texture[0][0] == 6


def test_print_grid_outputs_score_and_lives(capsys):
    game_map = make_map(
        [
            [0, 0],
            [0, 0],
        ],
        pellet_grid=[
            [PELLET, EMPTY],
            [EMPTY, EMPTY],
        ],
    )

    game_map.print_grid(points=42, health=2)
    output = capsys.readouterr().out

    assert "SCORE: 42" in output
    assert "LIVES: 2" in output
