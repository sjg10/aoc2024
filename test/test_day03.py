from ..days.day03 import *


def test_day03_p1():
    inp = "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"
    p1, _ = run(inp.splitlines())
    assert p1 == "161"


def test_day03_p2():
    inp = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"
    _, p2 = run(inp.splitlines())
    assert p2 == "48"
