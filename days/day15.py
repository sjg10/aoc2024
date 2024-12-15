from dataclasses import dataclass


@dataclass(frozen=True)
class Pos:
    r: int
    c: int

    def __add__(self, o):
        return Pos(self.r + o.r, self.c + o.c)

    def __sub__(self, o):
        return Pos(self.r - o.r, self.c - o.c)


class WarehouseBase:
    DIRMAP = {
        "^": Pos(-1, 0),
        "v": Pos(1, 0),
        ">": Pos(0, 1),
        "<": Pos(0, -1),
    }

    def __init__(self, map, ins, start):
        self.map = map
        self.ins = ins
        self.cur = start
        self.ins_cnt = 0

    def __getitem__(self, key: Pos):
        return self.map[key.r][key.c]

    def __setitem__(self, key: Pos, value):
        self.map[key.r][key.c] = value

    def __str__(self):
        ret = ""
        for r, l in enumerate(self.map):
            for c, x in enumerate(l):
                if Pos(r, c) == self.cur:
                    ret += "@"
                else:
                    ret += x
            ret += "\n"
        return ret


class Warehouse(WarehouseBase):
    def step(self):
        dir = Warehouse.DIRMAP[self.ins[self.ins_cnt]]
        nxt = self.cur + dir
        self.ins_cnt += 1
        if self[nxt] == ".":
            self.cur = nxt
        else:
            nxt_rob = nxt
            while True:
                match self[nxt]:
                    case "#":
                        break
                    case ".":
                        self[nxt] = "O"
                        self[nxt_rob] = "."
                        self.cur = nxt_rob
                        break
                nxt += dir

    def gps_sum(self):
        while self.ins_cnt < len(self.ins):
            self.step()
        ret = 0
        for r, l in enumerate(self.map):
            for c, x in enumerate(l):
                if x == "O":
                    ret += 100 * r + c
        return ret


class Warehouse2(WarehouseBase):
    def push_vert(self, r: int, cols: set[int], dir: int, updates=None):
        nextcols = set()
        if updates is None:
            updates = {}
        for c in cols:
            if Pos(r, c) not in updates:
                updates[Pos(r, c)] = "."
            if self[Pos(r + dir, c)] == "#":
                return None
            elif self[Pos(r + dir, c)] == ".":
                updates[Pos(r + dir, c)] = self[Pos(r, c)]
                pass
            elif self[Pos(r + dir, c)] == "[":
                nextcols.add(c)
                nextcols.add(c + 1)
                updates[Pos(r + dir, c)] = self[Pos(r, c)]
            elif self[Pos(r + dir, c)] == "]":
                nextcols.add(c)
                nextcols.add(c - 1)
                updates[Pos(r + dir, c)] = self[Pos(r, c)]
        if len(nextcols) == 0:
            return updates
        else:
            return self.push_vert(r + dir, nextcols, dir, updates)

    def step(self):
        dirch = self.ins[self.ins_cnt]
        dir = Warehouse.DIRMAP[dirch]
        nxt = self.cur + dir
        self.ins_cnt += 1
        if self[nxt] == ".":
            self.cur = nxt
        elif self[nxt] == "#":
            return  # On wall, dont move
        elif dirch == ">":
            nxt_rob = nxt
            while True:
                match self[nxt]:
                    case "#":
                        break
                    case ".":
                        while nxt != nxt_rob:
                            self[nxt] = "]"
                            nxt -= dir
                            self[nxt] = "["
                            nxt -= dir
                        self[nxt_rob] = "."
                        self.cur = nxt_rob
                        break
                nxt += dir
        elif dirch == "<":
            nxt_rob = nxt
            while True:
                match self[nxt]:
                    case "#":
                        break
                    case ".":
                        while nxt != nxt_rob:
                            self[nxt] = "["
                            nxt -= dir
                            self[nxt] = "]"
                            nxt -= dir
                        self[nxt_rob] = "."
                        self.cur = nxt_rob
                        break
                nxt += dir
        else:
            updates = self.push_vert(
                self.cur.r, set([self.cur.c]), -1 if dirch == "^" else 1
            )
            if updates is not None:  # could move
                self.cur = nxt
                for p in updates:
                    self[p] = updates[p]

    def gps_sum(self):
        while self.ins_cnt < len(self.ins):
            self.step()
        ret = 0
        for r, l in enumerate(self.map):
            for c, x in enumerate(l):
                if x == "[":
                    ret += 100 * r + c
        return ret


def build_warehouses(inlines):
    m = []
    m2 = []
    for r, l in enumerate(inlines):
        ls = l.strip()
        if len(ls) == 0:
            break
        else:
            m.append([])
            m2.append([])
            for c, x in enumerate(ls):
                match x:
                    case ".":
                        m2[-1].extend("..")
                        m[-1].append(".")
                    case "O":
                        m2[-1].extend("[]")
                        m[-1].append("O")
                    case "#":
                        m2[-1].extend("##")
                        m[-1].append("#")
                    case "@":  # hide the @ in the display
                        m2[-1].extend("..")
                        m[-1].append(".")
                        start1 = Pos(r, c)
                        start2 = Pos(r, c * 2)
    ins = ""
    for l in inlines:
        ins += l.strip()
    return Warehouse(m, ins, start1), Warehouse2(m2, ins, start2)


def run(inlines):
    w1, w2 = build_warehouses(inlines)
    return w1.gps_sum(), w2.gps_sum()
