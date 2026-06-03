import pytest

from src.stats import mean, median, variance


def test_mean_basic():
    assert mean([1, 2, 3, 4, 5]) == 3


def test_mean_single_value():
    assert mean([42]) == 42


def test_mean_empty_raises():
    with pytest.raises(ValueError):
        mean([])


def test_median_odd_count():
    assert median([3, 1, 2]) == 2


def test_median_even_count():
    assert median([1, 2, 3, 4]) == 2.5


def test_median_empty_raises():
    with pytest.raises(ValueError):
        median([])


def test_variance_basic():
    assert variance([2, 4, 4, 4, 5, 5, 7, 9]) == 4


def test_variance_constant_is_zero():
    assert variance([5, 5, 5, 5]) == 0


def test_variance_empty_raises():
    with pytest.raises(ValueError):
        variance([])
