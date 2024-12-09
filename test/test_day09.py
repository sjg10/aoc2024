from ..days.day09 import *


def test_day09():
    inp = """2333133121414131402"""
    p1, p2 = run(iter(inp.splitlines()))
    assert p1 == 1928
    assert p2 == 2858
