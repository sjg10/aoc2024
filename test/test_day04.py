from ..days.day04 import *


def test_day04():
    inp = """\
MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX
"""
    p1, p2 = run(inp.splitlines(keepends=True))
    assert p1 == "18"
    assert p2 == "9"
