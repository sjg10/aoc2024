import re
from functools import reduce
from operator import mul
from itertools import count


class Robot:
    def __init__(self, l, width, height):
        self.width = width
        self.height = height
        m = map(int, re.match(r"p=(-*\d*),(-*\d*) v=(-*\d*),(-*\d*)", l).groups())
        self.px = next(m)
        self.py = next(m)
        self.vx = next(m)
        self.vy = next(m)

    def get_pos(self, cycles):
        return (self.px + (self.vx * cycles)) % self.width, (
            self.py + (self.vy * cycles)
        ) % self.height

    def get_quadrant(self, cycles):
        p = self.get_pos(cycles)
        if p[0] < self.width // 2:
            if p[1] < self.height // 2:
                return 0
            if p[1] > self.height // 2:
                return 1
        if p[0] > self.width // 2:
            if p[1] < self.height // 2:
                return 2
            if p[1] > self.height // 2:
                return 3
        return None


def run(inlines, width=101, height=103, find_p2=True):
    qs = [0, 0, 0, 0]
    robots = []
    for l in inlines:
        robots.append(Robot(l, width, height))
        q = robots[-1].get_quadrant(100)
        if q is not None:
            qs[q] += 1
    p1 = reduce(mul, qs)

    # Find where a line of contiguous robots is -> there will be a xmas tree
    p2 = None
    if find_p2:
        for p2 in count(0):
            ret = [["." for j in range(width)] for k in range(height)]
            for r in robots:
                p = r.get_pos(p2)
                ret[p[1]][p[0]] = "#"
            out = ["".join(l) for l in ret]
            if any("###############################" in l for l in out):
                break
    return p1, p2
