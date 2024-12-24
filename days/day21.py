from dataclasses import dataclass
from itertools import permutations, product
from functools import cache


@dataclass(frozen=True, order=True)
class Pos:
    r: int
    c: int

    def __add__(self, o):
        return Pos(self.r + o.r, self.c + o.c)

    def __sub__(self, o):
        return Pos(self.r - o.r, self.c - o.c)


class NumPads:
    NUMLOCS = {
        "7": Pos(0, 0),
        "8": Pos(0, 1),
        "9": Pos(0, 2),
        "4": Pos(1, 0),
        "5": Pos(1, 1),
        "6": Pos(1, 2),
        "1": Pos(2, 0),
        "2": Pos(2, 1),
        "3": Pos(2, 2),
        "0": Pos(3, 1),
        "A": Pos(3, 2),
    }
    DLOCS = {
        "^": Pos(0, 1),
        "A": Pos(0, 2),
        "<": Pos(1, 0),
        "v": Pos(1, 1),
        ">": Pos(1, 2),
    }
    PTODIR = {
        "^": Pos(-1, 0),
        "<": Pos(0, -1),
        "v": Pos(1, 0),
        ">": Pos(0, 1),
    }

    def __init__(self, inlines):
        self.targets = []
        for l in inlines:
            self.targets.append(l.strip())

    def dirtostr(d):
        s = []
        if d.r < 0:
            s.append("^" * (-d.r))
        if d.r > 0:
            s.append("v" * (d.r))
        if d.c < 0:
            s.append("<" * (-d.c))
        if d.c > 0:
            s.append(">" * (d.c))
        return set("".join(x) for x in permutations(s))

    def badmove(cur, path, numpad):
        for p in path:
            cur = cur + NumPads.PTODIR[p]
            if numpad and cur == Pos(3, 0):
                return True
            if not numpad and cur == Pos(0, 0):
                return True
        return False

    @cache
    def get_shortest_path(pathsegment, robots):
        """
        For a single path segment of instructions ending with A,
        give the length of the shortest number of instructions
        to input this sequence, given number of robots above
        """
        cur = NumPads.DLOCS["A"]
        possible_presses = [""]
        for p in pathsegment:
            nxt = NumPads.DLOCS[p]
            newways = [
                x + "A"
                for x in filter(
                    lambda w: not NumPads.badmove(cur, w, False),
                    NumPads.dirtostr(nxt - cur),
                )
            ]
            possible_presses = ["".join(x) for x in product(possible_presses, newways)]
            cur = nxt
        if robots == 0:
            return min(len(x) for x in possible_presses)
        else:
            return min(
                sum(
                    NumPads.get_shortest_path(p + "A", robots - 1)
                    for p in w[:-1].split("A")
                )
                for w in possible_presses
            )

    def move(cur, target, num_dpad_robots):
        ways = [
            x + "A"
            for x in filter(
                lambda w: not NumPads.badmove(cur, w, True),
                NumPads.dirtostr(target - cur),
            )
        ]
        return min(NumPads.get_shortest_path(w, num_dpad_robots - 1) for w in ways)

    def run(self, midrobots):
        ret = 0
        for t in self.targets:
            shortest = 0
            lastdigit = "A"
            for digit in t:
                target = self.NUMLOCS[digit]
                x = NumPads.move(self.NUMLOCS[lastdigit], target, midrobots)
                shortest += x
                lastdigit = digit
            ret += shortest * int(t[:-1])
        return ret


def run(inlines):
    np = NumPads(inlines)
    return np.run(2), np.run(25)
