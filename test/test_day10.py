from ..days.day10 import *


def test_day10_1():
    inp = """\
...0...
...1...
...2...
6543456
7.....7
8.....8
9.....9"""
    p1, _ = run(inp.splitlines())
    assert p1 == 2


def test_day10_2():
    inp = """\
..90..9
...1.98
...2..7
6543456
765.987
876....
987...."""
    p1, _ = run(inp.splitlines())
    assert p1 == 4


def test_day10_3():
    inp = """\
89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732"""
    p1, p2 = run(inp.splitlines())
    assert p1 == 36
    assert p2 == 81
