from itertools import count


class ChronoSpatialComputer:
    def __init__(self, inlines):
        self.a_init = int(next(inlines).split()[2])
        self.b_init = int(next(inlines).split()[2])
        self.c_init = int(next(inlines).split()[2])
        next(inlines)  # skip empty
        self.prog = list(map(int, next(inlines).split()[1].split(",")))

    def get_combo(self):
        if self.prog[self.iptr + 1] < 4:
            return self.prog[self.iptr + 1]
        elif self.prog[self.iptr + 1] == 4:
            return self.a
        elif self.prog[self.iptr + 1] == 5:
            return self.b
        elif self.prog[self.iptr + 1] == 6:
            return self.c
        assert False

    def run(self, a_override=None):
        self.iptr = 0
        out = []
        self.a = self.a_init if a_override is None else a_override
        self.b = self.b_init
        self.c = self.c_init
        while self.iptr < len(self.prog):
            match self.prog[self.iptr]:
                case 0:
                    self.a //= pow(2, self.get_combo())
                case 1:
                    self.b ^= self.prog[self.iptr + 1]
                case 2:
                    self.b = self.get_combo() % 8
                case 3:
                    if self.a != 0:
                        self.iptr = self.prog[self.iptr + 1]
                        continue  # dont increment iptr
                case 4:
                    self.b ^= self.c
                case 5:
                    out.append(self.get_combo() % 8)
                case 6:
                    self.b = self.a // pow(2, self.get_combo())
                case 7:
                    self.c = self.a // pow(2, self.get_combo())
            self.iptr += 2
        return ",".join(map(str, out))

    def find_auto(self, aguess):
        pstr = ",".join(map(str, self.prog))
        rng = count(0) if aguess is None else range(*aguess)

        for a in rng:
            out = self.run(a, self.prog)
            if out == pstr:
                return a


def p2_real(csc):
    init = ""
    start = 0
    while True:
        for a in range(start, 8):
            testa = int(init + str(a), base=8)
            res = csc.run(testa)
            if int(res[0]) == csc.prog[-(len(init) + 1)]:
                init = init + str(a)
                start = 0
                break
        else:
            start = int(init[-1]) + 1
            init = init[:-1]
        if len(res.split(",")) == len(csc.prog):
            return int(init, base=8)


def run(inlines, p2real=True):
    csc = ChronoSpatialComputer(inlines)
    return csc.run(), p2_real(csc)
