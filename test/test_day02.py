from ..days.day02 import *


def test_day02():
    inp = """\
7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
"""
    p1, p2 = run(inp.splitlines())
    assert p1 == "2"
    assert p2 == "4"
