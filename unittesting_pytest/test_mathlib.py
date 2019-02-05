from . import mathlib
import pytest


@pytest.mark.skip()
def test_cal_total():
    total = mathlib.cal_total(2, 4)
    assert total == 6


def test_cal_multiply():
    mul = mathlib.cal_multiply(3, 5)
    assert mul == 15
