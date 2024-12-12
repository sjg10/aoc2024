from ..days.day12 import *


def test_day12_1():
    inp = """\
AAAA
BBCD
BBCC
EEEC"""
    p1, p2 = run(iter(inp.splitlines()))
    assert p1 == 140
    assert p2 == 80


def test_day12_2():
    inp = """\
OOOOO
OXOXO
OOOOO
OXOXO
OOOOO"""
    p1, p2 = run(iter(inp.splitlines()))
    assert p1 == 772
    assert p2 == 436


def test_day12_3():
    inp = """\
RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE"""
    p1, p2 = run(iter(inp.splitlines()))
    assert p1 == 1930
    assert p2 == 1206


def test_day12_4():
    inp = """\
EEEEE
EXXXX
EEEEE
EXXXX
EEEEE"""
    p1, p2 = run(iter(inp.splitlines()))
    assert p2 == 236


def test_day12_5():
    inp = """\
AAAAAA
AAABBA
AAABBA
ABBAAA
ABBAAA
AAAAAA"""
    p1, p2 = run(iter(inp.splitlines()))
    assert p2 == 368
