from ..days.day18 import *


def test_day18():
    inp = """\
5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0"""
    p1, p2 = run(iter(inp.splitlines()), 6, 6, 12)
    assert p1 == 22
    assert p2 == "6,1"
