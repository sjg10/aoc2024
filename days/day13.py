from itertools import batched
import re
from sympy import solve
from sympy.abc import a, b


def solve_machine(inp):
    ret1 = 0
    ret2 = 0
    m = re.match(r"Button A: X\+(\d*), Y\+(\d*)", inp[0])
    aX, aY = map(int, m.groups())
    m = re.match(r"Button B: X\+(\d*), Y\+(\d*)", inp[1])
    bX, bY = map(int, m.groups())
    m = re.match(r"Prize: X=(\d*), Y=(\d*)", inp[2])
    tX, tY = map(int, m.groups())
    tX2 = tX + 10000000000000
    tY2 = tY + 10000000000000
    sol1 = solve([(aX * a) + (bX * b) - tX, (aY * a) + (bY * b) - tY], [a, b])
    sol2 = solve([(aX * a) + (bX * b) - tX2, (aY * a) + (bY * b) - tY2], [a, b])
    if int(sol1[a]) == sol1[a] and int(sol1[b]) == sol1[b]:
        ret1 = sol1[a] * 3 + sol1[b]
    if int(sol2[a]) == sol2[a] and int(sol2[b]) == sol2[b]:
        ret2 = sol2[a] * 3 + sol2[b]
    return ret1, ret2


def run(inlines):
    ret1 = 0
    ret2 = 0
    for s in batched(inlines, 4):
        r1, r2 = solve_machine(s)
        ret1 += r1
        ret2 += r2
    return ret1, ret2
