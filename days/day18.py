from dataclasses import dataclass
from heapq import heappop, heappush


@dataclass(frozen=True)
class Pos:
    r: int
    c: int

    def __add__(self, o):
        return Pos(self.r + o.r, self.c + o.c)

    def __sub__(self, o):
        return Pos(self.r - o.r, self.c - o.c)

    def oob(self, rmax, cmax):
        return self.r < 0 or self.r > rmax or self.c < 0 or self.c > cmax

    def __lt__(self, o):
        return False  # To allow use in heap


class ProgramSpace:
    DIRS = [
        Pos(-1, 0),
        Pos(1, 0),
        Pos(0, 1),
        Pos(0, -1),
    ]

    def __init__(self, inlines, rmax, cmax):
        self.xs = []
        self.rmax = rmax
        self.cmax = cmax
        for l in inlines:
            ls = l.split(",")
            self.xs.append(Pos(int(ls[0]), int(ls[1])))

    def walk(self, blocks):
        """
        Dijkstra your way through to find shortest way out, or None if no exit
        """
        start_vertex = Pos(0, 0)
        visited = set()
        heap = [(0, start_vertex)]

        while len(heap) > 0:
            d, u = heappop(heap)

            if u.r == self.rmax and u.c == self.cmax:
                return d

            for dir in self.DIRS:
                nxt = u + dir
                if nxt.oob(self.rmax, self.cmax):
                    continue
                if nxt in blocks:
                    continue
                if nxt in visited:
                    continue
                visited.add(nxt)
                heappush(heap, (d + 1, nxt))
        return None

    def find_block(self, tstart):
        """
        Binary search from tstart to end of blocks to find first obstacle that prevents escape
        """
        lower = tstart
        upper = len(self.xs) + 1
        while upper > lower:
            x = (upper + lower) // 2
            if x == upper or x == lower:
                break
            blocks = set(self.xs[:x])
            if self.walk(blocks) is None:
                upper = x
            else:
                lower = x
        return f"{self.xs[x].r},{self.xs[x].c}"

    def find_path(self, p1max):
        """
        Find the shortest path to exit after p1max blocks fell
        """
        return self.walk(set(self.xs[:p1max]))


def run(inlines, rmax=70, cmax=70, p1max=1024):
    ps = ProgramSpace(inlines, rmax, cmax)
    return ps.find_path(p1max), ps.find_block(p1max + 1)
