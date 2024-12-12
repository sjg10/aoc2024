from dataclasses import dataclass, field
from enum import Enum


@dataclass(frozen=True)
class Pos:
    """
    Stores a pos. Fractional (+0.5) positions are perimeter pieces
    """

    r: float
    c: float

    def __lt__(x, y):
        return x.r < y.r or (x.r == y.r and x.c < y.c)

    def oob(self, maxr, maxc):
        return self.r < 0 or self.r > maxr or self.c < 0 or self.c > maxc

    def add(self, x):
        return Pos(self.r + x.r, self.c + x.c)

    def nbors(self):
        return [
            Pos(self.r, self.c + 1),
            Pos(self.r, self.c - 1),
            Pos(self.r + 1, self.c),
            Pos(self.r - 1, self.c),
        ]


class Direction(Enum):
    RIGHT = Pos(0, 1)
    DOWN = Pos(1, 0)
    LEFT = Pos(0, -1)
    UP = Pos(-1, 0)


# Operations to turn
@dataclass(frozen=True)
class Turn:
    move: Pos
    direction: Direction


# Given a direction, these are the possible new perimeter pieces to look at
turns = {
    Direction.RIGHT: [
        Turn(Pos(0.5, 0.5), Direction.DOWN),
        Turn(Pos(-0.5, 0.5), Direction.UP),
    ],
    Direction.DOWN: [
        Turn(Pos(0.5, 0.5), Direction.RIGHT),
        Turn(Pos(0.5, -0.5), Direction.LEFT),
    ],
    Direction.LEFT: [
        Turn(Pos(0.5, -0.5), Direction.DOWN),
        Turn(Pos(-0.5, -0.5), Direction.UP),
    ],
    Direction.UP: [
        Turn(Pos(-0.5, 0.5), Direction.RIGHT),
        Turn(Pos(-0.5, -0.5), Direction.LEFT),
    ],
}

# Direction to look for an adjacent space to a perimeter at a crossroads
cross_check = {
    Direction.RIGHT: Pos(-0.5, 0),
    Direction.DOWN: Pos(0, 0.5),
    Direction.LEFT: Pos(-0.5, 0),
    Direction.UP: Pos(0, 0.5),
}


class Region:
    def __init__(self, name):
        self.name = name
        self.contents = set()
        self.perimeter = set()

    def add_entry(self, x):
        self.contents.add(x)

    def add_perimeter(self, x, y):
        self.perimeter.add(Pos((x.r + y.r) / 2, (x.c + y.c) / 2))

    def get_perimeter_sides(self, prev=None, direction=Direction.RIGHT):
        if prev is None:  # First entry
            self.perimeter_visited = set()
        if prev is None or prev in self.perimeter_visited:
            # Already visited/ first entry
            # get unvisited perimeters
            rem = self.perimeter.difference(self.perimeter_visited)
            if len(rem) > 0:
                prev = min(rem)  # get top left unvisited
                direction = Direction.RIGHT
                # Check if we are going cw or ccw
                self.inside = int(
                    prev.r > 0 and Pos(prev.r - 0.5, prev.c) in self.contents
                )
            else:
                return 0
        self.perimeter_visited.add(prev)

        # Find if we can go straight, or have to turn
        next = prev.add(direction.value)
        if next in self.perimeter:
            if all(prev.add(x.move) in self.perimeter for x in turns[direction]):
                # We are at a cross roads - so we must turn instead of going straight
                if prev.add(cross_check[direction]) in self.contents:
                    t = turns[direction][self.inside]
                else:
                    t = turns[direction][1 - self.inside]
                return 1 + self.get_perimeter_sides(prev.add(t.move), t.direction)
            else:
                return self.get_perimeter_sides(next, direction)
        else:
            # Simple turn
            for t in turns[direction]:
                next = prev.add(t.move)
                if next in self.perimeter:
                    return 1 + self.get_perimeter_sides(next, t.direction)
        assert False  # shouldnt get here!

    def get_area(self):
        return len(self.contents)

    def get_perimeter_count(self):
        return len(self.perimeter)


class GardenMap:
    def __init__(self, inlines):
        self.map = []
        self.visited = []
        for r, l in enumerate(inlines):
            self.map.append(l.strip())
            self.visited.extend([False for i in range(len(self.map[-1]))])
        self.maxr = r
        self.maxc = len(l.strip()) - 1

    def get_next_unvisited(self):
        try:
            return Pos(*divmod(self.visited.index(False), self.maxr + 1))
        except ValueError:
            return None

    def mark_visited(self, x):
        loc = x.r * (self.maxr + 1) + x.c
        assert not self.visited[loc]
        self.visited[loc] = True

    def is_visited(self, x):
        loc = x.r * (self.maxr + 1) + x.c
        return self.visited[loc]

    def walk_region(self, start, r):
        self.mark_visited(start)
        r.add_entry(start)
        perimeter = 4
        for n in start.nbors():
            if n.oob(self.maxr, self.maxc):
                r.add_perimeter(start, n)
            elif self.map[n.r][n.c] != self.map[start.r][start.c]:
                r.add_perimeter(start, n)
            elif not self.is_visited(n):
                self.walk_region(n, r)

    def find_regions(self):
        p1 = 0
        p2 = 0
        n = self.get_next_unvisited()
        while n is not None:
            r = Region(self.map[n.r][n.c])
            self.walk_region(n, r)
            p1 += r.get_area() * r.get_perimeter_count()
            p2 += r.get_area() * r.get_perimeter_sides()

            n = self.get_next_unvisited()
        return p1, p2


def run(inlines):
    g = GardenMap(inlines)
    return g.find_regions()
