from dataclasses import dataclass


@dataclass(eq=True)
class Rule:
    left: str
    right: str
    op: str

    def apply(self, vals):
        match self.op:
            case "AND":
                return vals[self.left] & vals[self.right]
            case "OR":
                return vals[self.left] | vals[self.right]
            case "XOR":
                return vals[self.left] ^ vals[self.right]


class Grove:
    def __init__(self, inlines):
        self.initvals = {}
        for l in inlines:
            if len(l) <= 1:
                break
            wire, val = l.strip().split(": ")
            self.initvals[wire] = int(val)
        self.initrules = {}
        for l in inlines:
            left, op, right, _, out = l.strip().split()
            self.initrules[out] = Rule(left, right, op)

    def calc(self):
        rules = self.initrules.copy()
        vals = self.initvals.copy()
        while len(rules):
            rem = list(rules.keys())
            for out in rem:
                rule = rules[out]
                if rule.left in vals and rule.right in vals:
                    vals[out] = rule.apply(vals)
                    del rules[out]
        ret = 0
        idx = 0
        mul = 1
        while True:
            ptr = "z" + str(idx).zfill(2)
            if ptr not in vals:
                break
            ret += vals[ptr] * mul
            mul *= 2
            idx += 1
        return ret

    def findrule(self, left, right, op):
        a = [r for r in self.initrules if self.initrules[r] == Rule(left, right, op)]
        b = [r for r in self.initrules if self.initrules[r] == Rule(right, left, op)]
        if len(a) > 0:
            return a[0]
        elif len(b) > 0:
            return b[0]
        else:
            print(left, right, op)
            assert False

    def p2(self):
        # Found heuristically, using the code below
        swaps = [
            ("z10", "mwk"),
            ("z18", "qgd"),
            ("jmh", "hsw"),
            ("gqp", "z33"),
        ]
        for s in swaps:
            d0 = self.initrules[s[0]]
            d1 = self.initrules[s[1]]
            self.initrules[s[0]] = d1
            self.initrules[s[1]] = d0
        carries = {}

        # This is a sequence of 5 bit full adders. for each bit (except 0) we expect:
        # xi XOR yi -> ai_0
        # xi AND yi -> ai_1
        # ai_0 AND ci- -> ai_2
        # ai_2 OR ai_1- -> ci
        # ai_0 XOR ci- -> zi

        # Bit 0:
        id = str(0).zfill(2)
        assert self.initrules["z" + id] == Rule("x" + id, "y" + id, "XOR")
        carries[0] = self.findrule("x" + id, "y" + id, "AND")

        # Other bits
        for i in range(1, 45):
            id = str(i).zfill(2)
            a0 = self.findrule("x" + id, "y" + id, "XOR")
            a1 = self.findrule("x" + id, "y" + id, "AND")
            a2 = self.findrule(a0, carries[i - 1], "AND")
            carries[i] = self.findrule(a1, a2, "OR")
            assert "z" + id == self.findrule(a0, carries[i - 1], "XOR")

        rets = []
        for s in swaps:
            rets.append(s[0])
            rets.append(s[1])
        return ",".join(sorted(rets))


def run(inlines, p2=True):
    g = Grove(inlines)
    return g.calc(), g.p2() if p2 else None
