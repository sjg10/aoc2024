from dataclasses import dataclass
from enum import Enum
from collections import defaultdict
from heapq import heappop, heappush


@dataclass(frozen=True)
class Pos:
    r: int
    c: int

    def __add__(self, o):
        return Pos(self.r + o.r, self.c + o.c)


class Direction(Enum):
    EAST = Pos(0, 1)
    SOUTH = Pos(1, 0)
    WEST = Pos(0, -1)
    NORTH = Pos(-1, 0)

    def CW(self):
        match self.name:
            case "EAST":
                return Direction.SOUTH
            case "SOUTH":
                return Direction.WEST
            case "WEST":
                return Direction.NORTH
            case "NORTH":
                return Direction.EAST

    def CCW(self):
        match self.name:
            case "EAST":
                return Direction.NORTH
            case "SOUTH":
                return Direction.EAST
            case "WEST":
                return Direction.SOUTH
            case "NORTH":
                return Direction.WEST


@dataclass(frozen=True)
class PosD:
    p: Pos
    d: Direction

    def __lt__(self, other):
        return True  # unimportant, just needed so it can live in a heap


class ReindeerMaze:
    def __init__(self, inlines):
        self.locs = set()
        for r, l in enumerate(inlines):
            for c, x in enumerate(l.strip()):
                match x:
                    case ".":
                        self.locs.add(Pos(r, c))
                    case "S":
                        self.locs.add(Pos(r, c))
                        self.start = Pos(r, c)
                    case "E":
                        self.locs.add(Pos(r, c))
                        self.end = Pos(r, c)

    def walk(self):
        # Run dikstra but relax alt < dist to <= to get all paths
        start_vertex = PosD(self.start, Direction.EAST)
        dist = defaultdict(lambda: float("inf"))
        prev = defaultdict(set)
        heap = [(0, start_vertex)]

        while len(heap) > 0:
            d, u = heappop(heap)

            nxt = PosD(u.p + u.d.value, u.d)
            alt = d + 1
            if u not in prev[nxt] and nxt.p in self.locs and alt <= dist[nxt]:
                dist[nxt] = alt
                prev[nxt].add(u)
                heappush(heap, (alt, nxt))
            nxt = PosD(u.p, u.d.CW())
            alt = d + 1000
            if u not in prev[nxt] and alt <= dist[nxt]:
                dist[nxt] = alt
                prev[nxt].add(u)
                heappush(heap, (alt, nxt))
            nxt = PosD(u.p, u.d.CCW())
            alt = d + 1000
            if u not in prev[nxt] and alt <= dist[nxt]:
                dist[nxt] = alt
                prev[nxt].add(u)
                heappush(heap, (alt, nxt))

        # Now look at the endpoint(s), and get the min distance to end at any orientation
        endpts = [
            PosD(self.end, Direction.EAST),
            PosD(self.end, Direction.SOUTH),
            PosD(self.end, Direction.WEST),
            PosD(self.end, Direction.NORTH),
        ]
        mind = min(dist[x] for x in endpts)

        # Now loop through the endpts and iteratively get the previous steps
        pts = set(x for x in endpts if dist[x] == mind)
        lastpts = pts.copy()

        while len(lastpts) > 0:
            newpts = set()
            for u in lastpts:
                for x in prev[u]:
                    if x not in pts:
                        pts.add(x)
                        newpts.add(x)
            lastpts = newpts

        # Finally strip those paths down to only consider position, not direction
        ptsp = set(x.p for x in pts)

        return mind, len(ptsp)


def run(inlines):
    return ReindeerMaze(inlines).walk()
