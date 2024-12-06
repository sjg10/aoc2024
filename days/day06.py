from enum import Enum
from dataclasses import dataclass


class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


@dataclass(frozen=True)
class Pos:
    r: int
    c: int


@dataclass(frozen=True)
class PosD:
    p: Pos
    d: Direction


class Lab:
    def __init__(self, inlines):
        self.obstacles = set()
        for r, l in enumerate(inlines):
            for c, o in enumerate(l.strip()):
                match o:
                    case "#":
                        self.obstacles.add(Pos(r, c))
                    case "^":
                        self.guard = PosD(Pos(r, c), Direction.UP)
        self.maxc = c
        self.maxr = r
        self.path = set([self.guard.p])
        self.pathd = [self.guard]

    def _steppos(self, posd, extra_obstacle=None):
        match posd.d:
            case Direction.UP:
                if posd.p.r == 0:
                    return None
                nxt = Pos(posd.p.r - 1, posd.p.c)
                if nxt == extra_obstacle or nxt in self.obstacles:
                    return self._steppos(PosD(posd.p, Direction.RIGHT), extra_obstacle)
                else:
                    return PosD(nxt, posd.d)
            case Direction.RIGHT:
                if posd.p.c == self.maxc:
                    return None
                nxt = Pos(posd.p.r, posd.p.c + 1)
                if nxt == extra_obstacle or nxt in self.obstacles:
                    return self._steppos(PosD(posd.p, Direction.DOWN), extra_obstacle)
                else:
                    return PosD(nxt, posd.d)
            case Direction.DOWN:
                if posd.p.r == self.maxr:
                    return None
                nxt = Pos(posd.p.r + 1, posd.p.c)
                if nxt == extra_obstacle or nxt in self.obstacles:
                    return self._steppos(PosD(posd.p, Direction.LEFT), extra_obstacle)
                else:
                    return PosD(nxt, posd.d)
            case Direction.LEFT:
                if posd.p.c == 0:
                    return None
                nxt = Pos(posd.p.r, posd.p.c - 1)
                if nxt == extra_obstacle or nxt in self.obstacles:
                    return self._steppos(PosD(posd.p, Direction.UP), extra_obstacle)
                else:
                    return PosD(nxt, posd.d)

    def step(self):
        self.guard = self._steppos(self.guard)
        if self.guard is None:
            return False
        else:
            self.path.add(self.guard.p)
            self.pathd.append(self.guard)
            return True

    def get_covered(self):
        return len(self.path)

    def get_new_loops(self):
        tot = 0
        excluded = set([self.pathd[0].p])  # dont use the guard starting position
        # Obstacle must be on original path, try them all in order
        for i, x in enumerate(self.pathd):
            # don't retry a location
            if x.p in excluded:
                continue
            excluded.add(x.p)

            # Now keep track of all the previous steps (with direction)
            visited = set(self.pathd[: i - 1])
            # And start walking from just before the obstacle until revisit or leave the grid
            nxt = self.pathd[i - 1]
            while True:
                nxt = self._steppos(nxt, extra_obstacle=x.p)
                if nxt is None:  # left grid
                    break
                if nxt in visited:  # Revisit - loop!
                    tot += 1
                    break
                visited.add(nxt)
        return tot


def run(inlines):
    lab = Lab(inlines)
    while lab.step():  # walk to end
        pass
    return str(lab.get_covered()), str(lab.get_new_loops())
