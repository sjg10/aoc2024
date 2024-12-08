from itertools import combinations
from collections import defaultdict
from dataclasses import dataclass


@dataclass(frozen=True)
class Pos:
    r: int
    c: int

    def oob(self, maxr, maxc):
        """
        Return true if this node is out of grid bounds
        """
        if 0 <= self.r <= maxr and 0 <= self.c <= maxc:
            return False
        else:
            return True

    def anodes(self, p, maxr, maxc, singlepair=True):
        """
        Get the antinodes for this Pos to p.
        Return the ones in range of a maxr x maxc grid
        Optionally return type 1 (singlepair == True) or type 2 antinodes
        """
        ret = []
        rdiff = p.r - self.r
        cdiff = p.c - self.c
        for i in range(1, maxr):
            x = Pos(
                p.r + rdiff * i,
                p.c + cdiff * i,
            )
            if not x.oob(maxr, maxc):
                ret.append(x)
            else:
                break
            if singlepair:
                break
        for i in range(1, maxr):
            x = Pos(
                self.r - rdiff * i,
                self.c - cdiff * i,
            )
            if not x.oob(maxr, maxc):
                ret.append(x)
            else:
                break
            if singlepair:
                break
        return ret


class AntennaMap:
    def __init__(self, inlines):
        self.antennae = defaultdict(list)
        self.anodes1 = set()
        self.anodes2 = set()
        for r, l in enumerate(inlines):
            for c, o in enumerate(l.strip()):
                if o != ".":
                    self.antennae[o].append(Pos(r, c))
                    self.anodes2.add(Pos(r, c))
        self.maxc = c
        self.maxr = r

    def get_anodes(self):
        """
        Get the pair of antinodes of type 1 and type 2
        """
        for x in self.antennae:
            for a, b in combinations(self.antennae[x], 2):
                self.anodes1.update(a.anodes(b, self.maxr, self.maxc))
                self.anodes2.update(a.anodes(b, self.maxr, self.maxc, False))
        return len(self.anodes1), len(self.anodes2)


def run(inlines):
    amap = AntennaMap(inlines)
    return amap.get_anodes()
