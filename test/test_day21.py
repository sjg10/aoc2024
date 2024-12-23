from ..days.day21 import *


def test_day21():
    inp = """\
029A
980A
179A
456A
379A"""
    p1, p2 = run(iter(inp.splitlines()))
    assert p1 == 126384
