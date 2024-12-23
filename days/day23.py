from collections import defaultdict
from itertools import combinations


class LANParty:
    def __init__(self, inlines):
        self.nbors = defaultdict(set)
        self.ts = set()
        for l in inlines:
            a, b = l.strip().split("-")
            if a[0] == "t":
                self.ts.add(a)
            if b[0] == "t":
                self.ts.add(b)
            self.nbors[a].add(b)
            self.nbors[b].add(a)

    def get_ts(self):
        triples = set()
        for t in self.ts:
            for n1, n2 in combinations(self.nbors[t], 2):
                if n1 in self.nbors[n2]:
                    triples.add(frozenset([t, n1, n2]))
        return len(triples)

    def get_ll(self):
        C1 = []
        self.bors_kerbosch(set(), set(self.nbors.keys()), set(), C1)
        return ",".join(sorted(max(C1, key=len)))

    def bors_kerbosch(self, R, P, X, C):
        if len(P) == 0 and len(X) == 0:
            if len(R) > 2:
                C.append(R)
            return
        for v in P.union(set([])):
            self.bors_kerbosch(
                R.union(set([v])),
                P.intersection(self.nbors[v]),
                X.intersection(self.nbors[v]),
                C,
            )
            P.remove(v)
            X.add(v)


def run(inlines):
    nw = LANParty(inlines)
    return nw.get_ts(), nw.get_ll()
