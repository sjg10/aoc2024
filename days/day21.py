from dataclasses import dataclass
from heapq import heappop, heappush


@dataclass(frozen=True, order=True)
class Pos:
    r: int
    c: int

    def __add__(self, o):
        return Pos(self.r + o.r, self.c + o.c)

    def __sub__(self, o):
        return Pos(self.r - o.r, self.c - o.c)

    def dist(self, o):
        return abs(self.r - o.r) + abs(self.c - o.c)


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
    DLCI = {  # DLOCS inverted
        Pos(0, 1): "^",
        Pos(0, 2): "A",
        Pos(1, 0): "<",
        Pos(1, 1): "v",
        Pos(1, 2): ">",
    }

    def __init__(self, inlines):
        self.targets = []
        for l in inlines:
            self.targets.append(l.strip())

    @staticmethod
    def simulate(robots, target, depth=2):
        """
        Given robot positions, a final target, and a depth at which A is pressed:
        Simulate pressing A and if this gets us not further from target, return True, else False
        """
        push = False
        if depth > 1:  # A is pressed by a robot controlling a direction robot
            match NumPads.DLCI[robots[depth]]:
                case "^":
                    if robots[depth - 1].r != 0 and robots[depth - 1].c != 0:
                        robots[depth - 1] = Pos(
                            robots[depth - 1].r - 1, robots[depth - 1].c
                        )
                        push = True
                case "v":
                    if robots[depth - 1].r != 1:
                        robots[depth - 1] = Pos(
                            robots[depth - 1].r + 1, robots[depth - 1].c
                        )
                        push = True
                case ">":
                    if robots[depth - 1].c != 2:
                        robots[depth - 1] = Pos(
                            robots[depth - 1].r, robots[depth - 1].c + 1
                        )
                        push = True
                case "<":
                    if robots[depth - 1].c != 0 and (
                        robots[depth - 1].r != 0 or robots[depth - 1].c != 1
                    ):
                        robots[depth - 1] = Pos(
                            robots[depth - 1].r, robots[depth - 1].c - 1
                        )
                        push = True
                case "A":
                    push = NumPads.simulate(robots, target, depth - 1)
        else:  # A is pressed by a robot controlling a digit robot
            match NumPads.DLCI[robots[depth]]:
                case "^":
                    if robots[0].r != 0:
                        nr0 = Pos(robots[0].r - 1, robots[0].c)
                        if target.dist(nr0) < target.dist(robots[0]):
                            robots[0] = nr0
                            push = True
                case "v":
                    if robots[0].r != 3 and (robots[0].r != 2 or robots[0].c != 0):
                        nr0 = Pos(robots[0].r + 1, robots[0].c)
                        if target.dist(nr0) < target.dist(robots[0]):
                            robots[0] = nr0
                            push = True
                case ">":
                    if robots[depth - 1].c != 2:
                        nr0 = Pos(robots[0].r, robots[0].c + 1)
                        if target.dist(nr0) < target.dist(robots[0]):
                            robots[0] = nr0
                            push = True
                case "<":
                    if robots[0].c != 0 and (robots[0].c != 1 or robots[0].r != 3):
                        nr0 = Pos(robots[0].r, robots[0].c - 1)
                        if target.dist(nr0) < target.dist(robots[0]):
                            robots[0] = nr0
                            push = True
                case "A":  # Digit robot told to push - only allow correct target
                    if robots[0] == target:
                        push = True
        return push

    @staticmethod
    def move(cur, target):
        """
        Find the shortest input sequence to move from cur to target on the digit pad and press it
        """
        visited = set()
        # strlen, str, robot1 pos, robot2 pos, robot3 pos
        heap = [(0, "", cur, Pos(0, 2), Pos(0, 2))]
        while len(heap) > 0:
            d, u, r1, r2, r3 = heappop(heap)
            # dont go the opposite direction to last char - waste of a try
            last = u[-1] if len(u) else None

            if r1 == target:
                return u

            # Try each direction

            nxt = u + "^"
            if last != "v" and nxt not in visited and r3.r != 0 and r3.c != 0:
                visited.add(nxt)
                heappush(heap, (d + 1, nxt, r1, r2, Pos(r3.r - 1, r3.c)))

            nxt = u + "v"
            if last != "^" and nxt not in visited and r3.r != 1:
                visited.add(nxt)
                heappush(heap, (d + 1, nxt, r1, r2, Pos(r3.r + 1, r3.c)))

            nxt = u + ">"
            if last != "<" and nxt not in visited and r3.c != 2:
                visited.add(nxt)
                heappush(heap, (d + 1, nxt, r1, r2, Pos(r3.r, r3.c + 1)))

            nxt = u + "<"
            if (
                last != ">"
                and nxt not in visited
                and r3.c != 0
                and (r3.r != 0 or r3.c != 1)
            ):
                visited.add(nxt)
                heappush(heap, (d + 1, nxt, r1, r2, Pos(r3.r, r3.c - 1)))

            nxt = u + "A"
            if nxt not in visited:
                robots = [r1, r2, r3]
                push = NumPads.simulate(robots, target)
                if push:
                    visited.add(nxt)
                    heappush(heap, (d + 1, nxt, *robots))

    def p1(self):
        p1 = 0
        for t in self.targets:
            c = ""
            lastdigit = "A"
            for digit in t:
                target = self.NUMLOCS[digit]
                mv = NumPads.move(self.NUMLOCS[lastdigit], target)
                print(f"From {lastdigit} to {digit} = {mv}")
                c += mv
                lastdigit = digit
            print("DONE", t, c, len(c))
            p1 += len(c) * int(t[:-1])
        return p1


def run(inlines):
    np = NumPads(inlines)
    return np.p1(), None
