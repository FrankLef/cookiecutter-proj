"""Test the log1ps module."""
import pytest
import math
import src.helpers.log1ps as lg


@pytest.fixture
def x_vals():
    return (-100, -10, -1, -0.1, 0, 0.1, 1, 10, 100)


def test_log1ps(x=-math.e):
    out = lg.log1ps(x)
    target = -math.log(math.e + 1)
    assert math.isclose(out, target)


def test_expm1s(x=-math.log(math.e + 1)):
    out = lg.expm1s(x)
    target = -math.e
    assert math.isclose(out, target)


def test_log1ps10(x=-10):
    out = lg.log1ps10(x)
    target = -math.log(10 + 1, 10)
    assert math.isclose(out, target)


def test_expm1s10(x=-math.log(10 + 1, 10)):
    out = lg.expm1s10(x)
    target = -10
    assert math.isclose(out, target)


def test_logexp10(x=-0.1):
    out = lg.log1ps10(x)
    target = lg.expm1s10(out)
    # msg = f"{out} vs {target}"
    # print(msg)
    assert math.isclose(x, target)


def test_logexp(x_vals):
    lg_vals = lg.log1ps10(x_vals)
    nat_vals = lg.expm1s10(lg_vals)
    z = zip(x_vals, nat_vals)
    check = [math.isclose(item[0], item[1]) for item in z]
    assert all(check)
