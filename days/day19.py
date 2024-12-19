from functools import cache


class TowelSearch:
    def __init__(self, inlines):
        self.towels = next(inlines).strip().split(", ")
        self.patterns = set()
        print(self.towels)
        next(inlines)
        for l in inlines:
            self.patterns.add(l.strip())

    @cache
    def _search(self, p):
        if len(p) == 0:
            return 1
        ways = 0
        for towel in self.towels:
            if p.startswith(towel):
                ways += self._search(p[len(towel) :])
        return ways

    def run(self):
        p1 = 0
        p2 = 0
        for p in self.patterns:
            r = self._search(p)
            if r > 0:
                p1 += 1
                p2 += r
        return p1, p2


def run(inlines):
    ts = TowelSearch(inlines)
    return ts.run()
