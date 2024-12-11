from ..days.day11 import *


def test_day11():
    inp = """125 17"""
    p1, p2 = run(iter(inp.splitlines()))
    assert p1 == 55312
    assert p2 == 65601038650482
