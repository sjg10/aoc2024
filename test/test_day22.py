from ..days.day22 import *


def test_day22_1():
    assert evolve(123) == 15887950
    assert evolve(15887950) == 16495136


def test_day22():
    inp = """\
1
10
100
2024
"""
    p1, _ = run(iter(inp.splitlines()))
    assert p1 == 37327623


def test_day22_2():
    inp = """\
1
2
3
2024
"""
    _, p2 = run(iter(inp.splitlines()))
    assert p2 == 23
