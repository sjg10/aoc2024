from dataclasses import dataclass


@dataclass(frozen=True)
class Pos:
    r: int
    c: int

    def oob(self, maxr, maxc):
        return self.r < 0 or self.r > maxr or self.c < 0 or self.c > maxc


class LavaMap:
    def __init__(self, inlines):
        self.map = []
        self.zeros = []
        for r, l in enumerate(inlines):
            self.map.append([])
            for c, o in enumerate(l.strip()):
                if o == ".":
                    self.map[-1].append(".")
                else:
                    self.map[-1].append(int(o))
                if o == "0":
                    self.zeros.append(Pos(r, c))
        self.maxr = r
        self.maxc = c

    def walk(self, start):
        val = self.map[start.r][start.c]
        if val == 9:
            return set((start,)), 1
        nxt = [
            Pos(start.r, start.c + 1),
            Pos(start.r, start.c - 1),
            Pos(start.r + 1, start.c),
            Pos(start.r - 1, start.c),
        ]
        ret1 = set()
        ret2 = 0
        for x in nxt:
            if (
                not x.oob(self.maxr, self.maxc)
                and self.map[x.r][x.c] != "."
                and self.map[x.r][x.c] == val + 1
            ):
                r1, r2 = self.walk(x)
                ret1.update(r1)
                ret2 += r2
        return ret1, ret2

    def walk2(self, start):
        val = self.map[start.r][start.c]
        if val == 9:
            return 1
        nxt = [
            Pos(start.r, start.c + 1),
            Pos(start.r, start.c - 1),
            Pos(start.r + 1, start.c),
            Pos(start.r - 1, start.c),
        ]
        ret = 0
        for x in nxt:
            if (
                not x.oob(self.maxr, self.maxc)
                and self.map[x.r][x.c] != "."
                and self.map[x.r][x.c] == val + 1
            ):
                ret += self.walk2(x)
        return ret

    def find_paths(self):
        s1 = 0
        s2 = 0
        for start in self.zeros:
            a, b = self.walk(start)
            s1 += len(a)
            s2 += b
        return s1, s2


def run(inlines):
    lm = LavaMap(inlines)
    return lm.find_paths()
