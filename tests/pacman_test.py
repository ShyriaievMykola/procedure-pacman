import time
import pytest
import pacman
from constants import TUNNEL, WALL, PELLET, POWER, FRUIT, EMPTY
from map.game_map import GameMap
from ghosts.behaviors.scatter_behavior import ScatterBehavior
from ghosts.behaviors.frightened_behavior import FrightenedBehavior
from ghosts.behaviors.eaten_behavior import EatenBehavior
from ghosts.ghost_manager import GhostManager
import visualisation.config
from unittest.mock import patch

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def startfield():
    """
    4x4 map used by most tests.

    Grid (TUNNEL = passable, WALL = impassable):
        (0,0)T  (1,0)T  (2,0)T  (3,0)T
        (0,1)T  (1,1)W  (2,1)T  (3,1)T
        (0,2)T  (1,2)T  (2,2)T  (3,2)T
        (0,3)T  (1,3)T  (2,3)T  (3,3)T

    Pellet grid:
        EMPTY   PELLET  FRUIT   EMPTY
        EMPTY   EMPTY   POWER   EMPTY
        EMPTY   EMPTY   EMPTY   EMPTY
        EMPTY   EMPTY   EMPTY   EMPTY

    Ghosts initial positions:
        ghost[0] -> (1,2)
        ghost[1] -> (0,2)
        ghost[2] -> (0,1)
        ghost[3] -> (0,0)
    """
    map = GameMap()
    map.grid = [
        [TUNNEL, TUNNEL, TUNNEL, TUNNEL],
        [TUNNEL, WALL,   TUNNEL, TUNNEL],
        [TUNNEL, TUNNEL, TUNNEL, TUNNEL],
        [TUNNEL, TUNNEL, TUNNEL, TUNNEL],
    ]
    map.pellet_grid = [
        [EMPTY,  PELLET, FRUIT,  EMPTY],
        [EMPTY,  EMPTY,  POWER,  EMPTY],
        [EMPTY,  EMPTY,  EMPTY,  EMPTY],
        [EMPTY,  EMPTY,  EMPTY,  EMPTY],
    ]
    map.width = 4
    map.height = 4
    map.ghost_door = (2, 2)
    ghost_manager = GhostManager(map)
    ghost_manager.ghosts[0].position = (1, 2)
    ghost_manager.ghosts[0].old_position = (1, 2)
    ghost_manager.ghosts[1].position = (0, 2)
    ghost_manager.ghosts[1].old_position = (0, 2)
    ghost_manager.ghosts[2].position = (0, 1)
    ghost_manager.ghosts[2].old_position = (0, 1)
    ghost_manager.ghosts[3].position = (0, 0)
    ghost_manager.ghosts[3].old_position = (0, 0)
    visualisation.config.state = visualisation.config.play_state.PLAYING
    return map, ghost_manager


def reset_pacman(pos=(0, 3)):
    """Reset all global pacman state before each test."""
    pacman.position = pos
    pacman.old_position = pos
    pacman.movement_direction = (0, 0)
    pacman.pending_direction = (0, 0)
    pacman.points = 0
    pacman.health = pacman.max_health
    pacman.empowered = False
    pacman.almost_lost_power = False
    pacman.last_power_time = 0.0
    pacman.invincible = False
    pacman.invincible_start_time = 0.0
    pacman.points_for_ghost = pacman.starting_points_for_ghost
    visualisation.config.state = visualisation.config.play_state.PLAYING


# ---------------------------------------------------------------------------
# get_spawn_position
# ---------------------------------------------------------------------------
@pytest.mark.pac_spawn
class TestGetSpawnPosition:
    def test_returns_first_tunnel_with_pellet(self):
        map, _ = startfield()
        x, y = pacman.get_spawn_position(map)
        assert map.grid[y][x] == TUNNEL
        assert map.pellet_grid[y][x] == PELLET \
               or map.pellet_grid[y][x] == EMPTY

    def test_spawn_is_correct_cell(self):
        map, _ = startfield()
        # First TUNNEL cell with a PELLET in our map is (1, 0)
        assert pacman.get_spawn_position(map) == (1, 0)


# ---------------------------------------------------------------------------
# Movement – resolve_pend
# ---------------------------------------------------------------------------
@pytest.mark.pac_movement
class TestMovement:
    @pytest.fixture
    def game(self):
        map, gm = startfield()
        reset_pacman(pos=(0, 3))
        return map, gm

    def test_moves_in_pending_direction_when_clear(self, game):
        map, gm = game
        pacman.pending_direction = (1, 0)   # move right
        pacman.resolve_pend(map, None)
        assert pacman.position == (1, 3)

    def test_pending_becomes_movement_direction(self, game):
        map, gm = game
        pacman.pending_direction = (1, 0)
        pacman.resolve_pend(map, None)
        assert pacman.movement_direction == (1, 0)

    def test_falls_back_to_movement_direction_when_pending_blocked(self, game):
        # pacman at (0,1), pending=right -> (1,1) is WALL
        # movement=down -> (0,2) is TUNNEL -> should move there
        map, gm = game
        pacman.position = (0, 1)
        pacman.old_position = (0, 1)
        pacman.pending_direction = (1, 0)   # right -> WALL at (1,1)
        pacman.movement_direction = (0, 1)   # down  -> TUNNEL at (0,2)
        pacman.resolve_pend(map, None)
        assert pacman.position == (0, 2)

    def test_stays_in_place_when_both_directions_blocked(self, game):
        # pacman at (0,1), pending=right->WALL, movement=(0,0)->no movement
        map, gm = game
        pacman.position = (0, 1)
        pacman.old_position = (0, 1)
        pacman.pending_direction = (1, 0)   # right -> WALL at (1,1)
        pacman.movement_direction = (0, 0)   
        # standing still -> new pos == current pos -> not a wall
        # With (0,0) direction new pos == current pos 
        # which is TUNNEL, so pacman stays on same cell
        before = pacman.position
        pacman.resolve_pend(map, None)
        assert pacman.position == before

    def test_old_position_is_saved_before_move(self, game):
        map, gm = game
        pacman.position = (0, 3)
        pacman.old_position = (0, 3)
        pacman.pending_direction = (1, 0)
        pacman.resolve_pend(map, None)
        assert pacman.old_position == (0, 3)

    def test_cannot_move_into_wall(self, game):
        # (0,1) -> right -> (1,1) is WALL, no current direction -> stays
        map, gm = game
        pacman.position = (0, 1)
        pacman.old_position = (0, 1)
        pacman.pending_direction = (1, 0)
        pacman.movement_direction = (0, 0)
        pacman.resolve_pend(map, None)
        assert pacman.position == (0, 1)

    def test_position_clamped_to_map_bounds(self, game):
        map, gm = game
        pacman.position = (0, 0)
        pacman.old_position = (0, 0)
        pacman.pending_direction = (-1, 0)   # would go out of bounds left
        pacman.resolve_pend(map, None)
        assert pacman.position[0] >= 0
        assert pacman.position[1] >= 0


# ---------------------------------------------------------------------------
# Eating – pellets, power pellets, fruits
# ---------------------------------------------------------------------------
@pytest.mark.pac_eating
class TestEating:
    @pytest.fixture
    def game(self):
        map, gm = startfield()
        reset_pacman(pos=(0, 3))
        return map, gm

    def test_eat_pellet_increases_points(self, game):
        map, gm = game
        pacman.position = (1, 0)
        pacman.eat((1, 0), map, None)
        assert pacman.points == 1

    def test_eat_pellet_empties_cell(self, game):
        map, gm = game
        pacman.position = (1, 0)
        pacman.eat((1, 0), map, None)
        assert map.pellet_grid[0][1] == EMPTY

    def test_eat_fruit_increases_points_by_fruit_value(self, game):
        map, gm = game
        pacman.position = (2, 0)
        pacman.eat((2, 0), map, None)
        assert pacman.points == pacman.fruit_value

    def test_eat_fruit_empties_cell(self, game):
        map, gm = game
        pacman.position = (2, 0)
        pacman.eat((2, 0), map, None)
        assert map.pellet_grid[0][2] == EMPTY

    def test_eat_power_pellet_enables_empowered(self, game):
        map, gm = game
        pacman.position = (2, 1)
        pacman.eat((2, 1), map, None)
        assert pacman.empowered is True

    def test_eat_power_pellet_sets_last_power_time(self, game):
        map, gm = game
        before = time.time()
        pacman.position = (2, 1)
        pacman.eat((2, 1), map, None)
        assert pacman.last_power_time >= before

    def test_eat_power_pellet_empties_cell(self, game):
        map, gm = game
        pacman.position = (2, 1)
        pacman.eat((2, 1), map, None)
        assert map.pellet_grid[1][2] == EMPTY

    def test_eating_last_pellet_triggers_victory(self, game):
        map, gm = game
        # Clear all pellets except one
        for y in range(map.height):
            for x in range(map.width):
                map.pellet_grid[y][x] = EMPTY
        map.pellet_grid[0][1] = PELLET
        pacman.position = (1, 0)
        pacman.eat((1, 0), map, None)
        assert visualisation.config.state == visualisation.config.play_state.VICTORY

    def test_empty_cell_does_nothing_to_points(self, game):
        map, gm = game
        pacman.position = (0, 0)
        pacman.eat((0, 0), map, None)
        assert pacman.points == 0


@pytest.mark.pac_tunnels
class TestTunnels:
    @pytest.fixture
    def game(self):
        map, gm = startfield()
        map.passage_left = (0, 2)
        map.passage_right = (3, 2)
        reset_pacman(pos=(0, 2))
        return map, gm

    @pytest.mark.parametrize("func, start, end", [
        (lambda m, p: p.go_through_passage_left(m), (0, 2), (3, 2)),   # left passage -> right passage
        (lambda m, p: p.go_through_passage_right(m), (3, 2), (0, 2)),   # right passage -> left
    ])
    def test_passage(self, game, func, start, end):
        map, gm = game
        pacman.position = start
        func(map, pacman)
        assert pacman.position == end

    @pytest.mark.parametrize("func, start, end", [
        (lambda m, p: p.go_through_passage_left(m), (0, 2), (3, 2)),   # left passage -> right passage
        (lambda m, p: p.go_through_passage_right(m), (3, 2), (0, 2)),   # right passage -> left
    ])
    def test_eat_dispatches(self, game, func, start, end):
        map, gm = game
        pacman.position = start
        pacman.eat(start, map, None)
        assert pacman.position == end


@pytest.mark.pac_ghosts
class TestGhostInteraction:
    @pytest.fixture
    def game(self):
        map, gm = startfield()
        reset_pacman(pos=(0, 3))
        return map, gm

    def _frighten_all(self, game):
        map, gm = game
        for g in gm.ghosts:
            g.strategy = FrightenedBehavior(g, map.width, map.height)

    @pytest.mark.parametrize("strategy", [
        lambda g: FrightenedBehavior(g, 4, 4),
        lambda g: ScatterBehavior("red", 4, 4),
        lambda g: EatenBehavior(g, 4, 4, (2, 2))
    ])
    def test_touch_ghost_loses_health_when_not_empowered(self, game, strategy):
        map, gm = game
        ghost = gm.ghosts[0]
        ghost.strategy = strategy(ghost)
        pacman.touch_ghost(gm, ghost)
        if isinstance(ghost.strategy, FrightenedBehavior) or isinstance(ghost.strategy, EatenBehavior):
            # Frightened or eaten ghosts are edible, so no health loss
            assert pacman.health == pacman.max_health
        else:
            # Non-frightened ghosts cause health loss
            assert pacman.health == pacman.max_health - 1

    @pytest.mark.parametrize("strategy", [
        lambda g: FrightenedBehavior(g, 4, 4),
        lambda g: ScatterBehavior("red", 4, 4),
        lambda g: EatenBehavior(g, 4, 4, (2, 2))
    ])
    def test_touch_ghost_triggers_game_over_on_last_life(self, game, strategy):
        map, gm = game
        pacman.health = 1
        ghost = gm.ghosts[0]
        ghost.strategy = strategy(ghost)
        pacman.touch_ghost(gm, ghost)
        if isinstance(ghost.strategy, FrightenedBehavior) or isinstance(ghost.strategy, EatenBehavior):
            # Frightened or eaten ghosts are edible, so no game over
            assert visualisation.config.state != visualisation.config.play_state.GAME_OVER
        else:
            assert visualisation.config.state == visualisation.config.play_state.GAME_OVER

    @pytest.mark.parametrize("strategy", [
        lambda g: FrightenedBehavior(g, 4, 4),
        lambda g: ScatterBehavior("red", 4, 4),
        lambda g: EatenBehavior(g, 4, 4, (2, 2))
    ])
    def test_touch_ghost_no_game_over_if_health_remains(self, game, strategy):
        map, gm = game
        pacman.health = 2
        ghost = gm.ghosts[0]
        ghost.strategy = strategy(ghost)
        pacman.touch_ghost(gm, ghost)
        assert visualisation.config.state != visualisation.config.play_state.GAME_OVER

    def test_eat_ghost_when_empowered_and_frightened(self, game):
        map, gm = game
        pacman.empowered = True
        self._frighten_all(game)
        ghost = gm.ghosts[0]
        pacman.touch_ghost(gm, ghost)
        assert pacman.points == pacman.starting_points_for_ghost
        assert ghost.strategy.__class__ == EatenBehavior
        assert pacman.health == pacman.max_health

    def test_ghost_score_doubles_per_chain(self, game):
        map, gm = game
        pacman.empowered = True
        self._frighten_all(game)
        pacman.touch_ghost(gm, gm.ghosts[0])   # 200
        assert pacman.points == 200
        self._frighten_all(game)
        pacman.touch_ghost(gm, gm.ghosts[1])   # 400
        assert pacman.points == 200 + 400
        self._frighten_all(game)
        pacman.touch_ghost(gm, gm.ghosts[2])   # 800
        assert pacman.points == 200 + 400 + 800

    def test_does_touch_ghost_same_cell(self, game):
        map, gm = game
        pacman.position = (1, 2)
        pacman.old_position = (0, 2)
        ghost = gm.ghosts[0]   # position = (1,2)
        assert pacman.does_touch_ghost(ghost) is True

    def test_does_touch_ghost_swap(self, game):
        map, gm = game
        # Pac moves (0,2)->(1,2), ghost moves (1,2)->(0,2) — they swapped cells
        pacman.position = (1, 2)
        pacman.old_position = (0, 2)
        ghost = gm.ghosts[0]
        ghost.position = (0, 2)
        ghost.old_position = (1, 2)
        assert pacman.does_touch_ghost(ghost) is True

    def test_does_touch_ghost_no_contact(self, game):
        map, gm = game
        pacman.position = (3, 3)
        pacman.old_position = (3, 2)
        ghost = gm.ghosts[0]   # at (1,2)
        assert pacman.does_touch_ghost(ghost) is False

    def test_get_touched_ghost_returns_all_touching(self, game):
        map, gm = game
        pacman.position = (1, 2)
        pacman.old_position = (1, 2)
        touching = pacman.get_touched_ghost(pacman.position, gm)
        positions = [g.position for g in touching]
        assert (1, 2) in positions

    def test_eaten_ghost_does_not_damage_pacman(self, game):
        map, gm = game
        ghost = gm.ghosts[0]
        ghost.strategy = EatenBehavior(ghost, map.width, map.height, map.ghost_door)
        pacman.touch_ghost(gm, ghost)
        assert pacman.health == pacman.max_health


@pytest.mark.pac_timers
class TestPowerTimer:
    def setup_method(self):
        reset_pacman()

    def test_empowered_turns_off_after_power_span(self):
        pacman.empowered = True
        pacman.last_power_time = time.time() - pacman.power_span - 0.1
        with patch('time.time', return_value=pacman.last_power_time + pacman.power_span + 0.1):
            pacman.maybe_lose_power()
        assert pacman.empowered is False

    def test_points_for_ghost_reset_after_power_expires(self):
        pacman.empowered = True
        pacman.points_for_ghost = 1600
        pacman.last_power_time = time.time()
        with patch('time.time', return_value=pacman.last_power_time + pacman.power_span + 0.1):
            pacman.maybe_lose_power()
        assert pacman.points_for_ghost == pacman.starting_points_for_ghost

    def test_still_empowered_within_span(self):
        pacman.empowered = True
        pacman.last_power_time = time.time()
        with patch('time.time', return_value=pacman.last_power_time + pacman.power_span - 0.1):
            pacman.maybe_lose_power()
        assert pacman.empowered is True


@pytest.mark.pac_state
class TestGameState:
    def setup_method(self):
        reset_pacman()

    def test_game_over_sets_state(self):
        pacman.game_over()
        assert visualisation.config.state == visualisation.config.play_state.GAME_OVER

    def test_victory_sets_state(self):
        pacman.victory()
        assert visualisation.config.state == visualisation.config.play_state.VICTORY
