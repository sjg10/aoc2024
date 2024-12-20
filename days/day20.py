from dataclasses import dataclass
from collections import defaultdict


@dataclass(frozen=True)
class Pos:
    r: int
    c: int

    def __add__(self, o):
        return Pos(self.r + o.r, self.c + o.c)

    def dist(self, o):
        return abs(self.r - o.r) + abs(self.c - o.c)


class RaceTrack:
    DIRS = [
        Pos(0, 1),
        Pos(0, -1),
        Pos(1, 0),
        Pos(-1, 0),
    ]

    def __init__(self, inlines):
        self.map = set()
        for r, l in enumerate(inlines):
            for c, x in enumerate(l.strip()):
                if x == "#":
                    continue
                else:
                    loc = Pos(r, c)
                    self.map.add(loc)
                    if x == "S":
                        self.start = loc
                    elif x == "E":
                        self.end = loc

    def walk(self, p1limit, p2limit):
        cur = self.start
        self.path = {cur: 0}
        self.shortcuts = defaultdict(int)
        self.longshortcuts = defaultdict(int)
        while cur != self.end:
            for d in self.DIRS:
                nxt = cur + d
                if nxt in self.map and nxt not in self.path:
                    break
            else:
                assert False
            for prev in self.path:
                shortdist = nxt.dist(prev)
                pathdist = self.path[cur] + 1 - self.path[prev]
                if shortdist == 2 and pathdist - shortdist > 0:
                    self.shortcuts[pathdist - shortdist] += 1
                if shortdist >= 2 and shortdist <= 20 and pathdist - shortdist > 0:
                    self.longshortcuts[pathdist - shortdist] += 1
            self.path[nxt] = self.path[cur] + 1
            cur = nxt
        return sum(self.shortcuts[x] for x in self.shortcuts if x >= p1limit), sum(
            self.longshortcuts[x] for x in self.longshortcuts if x >= p2limit
        )


def run(inlines, p1limit=100, p2limit=100):
    rt = RaceTrack(inlines)
    return rt.walk(p1limit, p2limit)
