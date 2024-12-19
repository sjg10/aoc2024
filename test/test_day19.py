from ..days.day19 import *


def test_day19():
    inp = """\
r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb"""
    p1, p2 = run(iter(inp.splitlines()))
    assert p1 == 6
    assert p2 == 16
