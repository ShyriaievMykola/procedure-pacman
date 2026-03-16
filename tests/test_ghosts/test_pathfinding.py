import pytest
from ghosts.utils.pathfinding import a_star
from constants import TUNNEL, WALL

@pytest.fixture
def grid():
    # Маленький лабіринт зі стіною посередині
    return [
        [TUNNEL, TUNNEL, TUNNEL],
        [TUNNEL, WALL,   TUNNEL],
        [TUNNEL, TUNNEL, TUNNEL]
    ]

def test_straight_path():
    # Шлях по прямій зверху вниз
    grid_plain = [[TUNNEL, TUNNEL, TUNNEL]]
    path = a_star(grid_plain, (0, 0), (2, 0))
    assert path == [(1, 0), (2, 0)]

def test_path_around_wall(grid):
    # Шлях з (0,0) в (2,2) в обхід стіни на (1,1)
    path = a_star(grid, (0, 0), (2, 2))
    assert (1, 1) not in path # Не йде крізь стіну
    assert len(path) > 0

def test_unreachable_goal():
    # Ціль повністю заблокована стінами
    blocked_grid = [
        [TUNNEL, WALL, TUNNEL],
        [WALL,   WALL, WALL],
        [TUNNEL, WALL, TUNNEL]
    ]
    # Алгоритм має повернути шлях до найближчої точки, а не впасти з помилкою
    path = a_star(blocked_grid, (0, 0), (2, 2))
    assert isinstance(path, list)

def test_start_is_goal():
    grid_plain = [[TUNNEL, TUNNEL]]
    path = a_star(grid_plain, (0, 0), (0, 0))
    assert path == []