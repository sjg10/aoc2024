from ..days.day17 import *


def test_day17():
    inp = """\
Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0"""
    csc = ChronoSpatialComputer(iter(inp.splitlines()))
    assert csc.run() == "4,6,3,5,6,3,5,2,1,0"
    # assert p2 == 45


def test_day17_3():
    inp = """\
Register A: 10
Register B: 0
Register C: 0

Program: 5,0,5,1,5,4"""
    csc = ChronoSpatialComputer(iter(inp.splitlines()))
    assert csc.run() == "0,1,2"


def test_day17_4():
    inp = """\
Register A: 2024
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0"""
    csc = ChronoSpatialComputer(iter(inp.splitlines()))
    assert csc.run() == "4,2,5,6,7,7,7,7,3,1,0"


def test_day17_5():
    inp = """\
Register A: 0
Register B: 29
Register C: 0

Program: 1,7"""
    csc = ChronoSpatialComputer(iter(inp.splitlines()))
    csc.run()
    assert csc.b == 26


def test_day17_6():
    inp = """\
Register A: 0
Register B: 2024
Register C: 43690

Program: 4,0"""
    csc = ChronoSpatialComputer(iter(inp.splitlines()))
    csc.run()
    assert csc.b == 44354


def test_day17_7():
    inp = """\
Register A: 2024
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0
"""
    p1, p2 = run(iter(inp.splitlines()), False)
    assert p2 == 117440
