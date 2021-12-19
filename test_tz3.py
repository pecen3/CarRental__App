import pytest
import time
from tz3 import max, min, sum, mult


def test_max():
    test_cases= [
        ('data.txt', 12),
    ]
    for file, result in test_cases:
        assert result == max(file)


def test_min():
    assert min('data.txt') == 1


def test_sum():
    assert sum('data.txt') == 78


def test_mult():
    assert mult('data.txt') == 479001600


def test_time():
    start_time1 = time.perf_counter()
    sum('time1.txt')
    finish_time1 = time.perf_counter() - start_time1
    start_time2 = time.perf_counter()
    sum('time2.txt')
    finish_time2 = time.perf_counter() - start_time2
    assert finish_time2/finish_time1 > 1


def test_letter():
    assert min('numbers_with_letter.txt') == 1
    assert max('numbers_with_letter.txt') == 12
    assert sum('numbers_with_letter.txt') == 78
    assert mult('numbers_with_letter.txt') == 479001600
