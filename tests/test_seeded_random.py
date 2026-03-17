import pytest

from seeded_random import SeededRandom


pytestmark = [pytest.mark.seeded_random]


def test_randint_sequence_is_deterministic_for_same_seed():
    a = SeededRandom(12345)
    b = SeededRandom(12345)

    seq_a = [a.randint(0, 1000) for _ in range(20)]
    seq_b = [b.randint(0, 1000) for _ in range(20)]

    assert seq_a == seq_b


def test_randfloat_sequence_is_deterministic_for_same_seed():
    a = SeededRandom(999)
    b = SeededRandom(999)

    seq_a = [a.randfloat() for _ in range(10)]
    seq_b = [b.randfloat() for _ in range(10)]

    assert seq_a == seq_b


def test_randfloat_is_always_in_half_open_interval():
    sr = SeededRandom(77)

    for _ in range(100):
        value = sr.randfloat()
        assert 0.0 <= value < 1.0


def test_randchance_zero_boundary(monkeypatch):
    sr = SeededRandom(1)

    monkeypatch.setattr(sr.srand, "randint", lambda _a, _b: 0)
    assert sr.randchance(0) is True

    monkeypatch.setattr(sr.srand, "randint", lambda _a, _b: 1)
    assert sr.randchance(0) is False


def test_randchance_hundred_boundary(monkeypatch):
    sr = SeededRandom(1)

    # Для 100% шансу навіть найбільше значення з randint(0,100) має проходити.
    monkeypatch.setattr(sr.srand, "randint", lambda _a, _b: 100)
    assert sr.randchance(100) is True


def test_randchance_middle_boundary(monkeypatch):
    sr = SeededRandom(1)

    monkeypatch.setattr(sr.srand, "randint", lambda _a, _b: 50)
    assert sr.randchance(50) is True

    monkeypatch.setattr(sr.srand, "randint", lambda _a, _b: 51)
    assert sr.randchance(50) is False
