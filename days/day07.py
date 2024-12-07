from itertools import product
from multiprocessing import Pool


def calc(t, p):
    for ops in product(["+", "*"], repeat=len(p) - 1):
        ans = p[0]
        for i in range(len(p) - 1):
            match ops[i]:
                case "+":
                    ans += p[i + 1]
                case "*":
                    ans *= p[i + 1]
        if ans == t:
            return t
    return 0


def calc2(t, p):
    for ops in product(["+", "*", "||"], repeat=len(p) - 1):
        ans = p[0]
        for i in range(len(p) - 1):
            match ops[i]:
                case "+":
                    ans += p[i + 1]
                case "*":
                    ans *= p[i + 1]
                case "||":
                    ans = int(str(ans) + str(p[i + 1]))
        if ans == t:
            return t
    return 0


def run(inlines):
    pool = Pool()
    r1 = []
    r2 = []
    for l in inlines:
        t, p = l.split(":")
        p = list(map(int, p.split()))
        t = int(t)
        r1.append(pool.apply_async(calc, (t, p)))
        r2.append(pool.apply_async(calc2, (t, p)))
    return str(sum(r.get() for r in r1)), str(sum(r.get() for r in r2))
