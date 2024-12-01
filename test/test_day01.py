from ..days.day01 import *


def test_day01():
    inp = """\
3   4
4   3
2   5
1   3
3   9
3   3
"""
    p1, p2 = run(inp.splitlines())
    assert p1 == "11"
    assert p2 == "31"
