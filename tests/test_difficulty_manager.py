import pytest

from difficulty_manager import DifficultyManager


pytestmark = [pytest.mark.difficulty_manager]


class DummyDifficultyConfig:
    def __init__(self):
        self.GHOST_SPEED_MS = 0
        self.PACMAN_SPEED_MS = 0


@pytest.fixture
def manager_and_config():
    cfg = DummyDifficultyConfig()
    return DifficultyManager(cfg), cfg


def test_set_easy_sets_expected_values(manager_and_config):
    manager, cfg = manager_and_config

    manager.set_easy()

    assert cfg.GHOST_SPEED_MS == 190
    assert cfg.PACMAN_SPEED_MS == 170


def test_set_medium_sets_expected_values(manager_and_config):
    manager, cfg = manager_and_config

    manager.set_medium()

    assert cfg.GHOST_SPEED_MS == 190
    assert cfg.PACMAN_SPEED_MS == 190


def test_set_hard_sets_expected_values(manager_and_config):
    manager, cfg = manager_and_config

    manager.set_hard()

    assert cfg.GHOST_SPEED_MS == 170
    assert cfg.PACMAN_SPEED_MS == 190


def test_set_custom_scales_from_base_speed(manager_and_config):
    manager, cfg = manager_and_config

    manager.set_custom(per_pacman=50, per_ghost=80)

    assert cfg.PACMAN_SPEED_MS == 95
    assert cfg.GHOST_SPEED_MS == 152


@pytest.mark.parametrize(
    "level, expected_pacman, expected_ghost",
    [
        (1, 220, 400),
        (2, 190, 325),
        (3, 160, 250),
        (4, 130, 175),
        (5, 100, 100),
    ],
)
def test_set_difficulty_levels(level, expected_pacman, expected_ghost, manager_and_config):
    manager, cfg = manager_and_config

    manager.set_difficulty(level)

    assert cfg.PACMAN_SPEED_MS == expected_pacman
    assert cfg.GHOST_SPEED_MS == expected_ghost


def test_set_difficulty_never_makes_ghost_faster_than_allowed(manager_and_config):
    manager, cfg = manager_and_config

    for level in range(1, 6):
        manager.set_difficulty(level)
        # За реалізацією GHOST_SPEED_MS не має бути меншим за PACMAN_SPEED_MS.
        assert cfg.GHOST_SPEED_MS >= cfg.PACMAN_SPEED_MS
