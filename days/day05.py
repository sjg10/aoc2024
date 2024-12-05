def processline(orders, x, part1=True):
    """
    Process a print x against orders.
    If in order return score, True
    Else reorder and return reordered_score, False
    """
    seen = set()
    for i in range(len(x)):
        diff = seen.difference(orders[x[i]])
        if len(diff) > 0:
            j = x.index(next(iter(diff)))
            x[i], x[j] = x[j], x[i]
            return processline(orders, x, False)
        seen.add(x[i])
    else:
        return x[len(x) // 2], part1


def run(inlines):
    res1 = 0
    res2 = 0
    orders = [set() for i in range(100)]
    for l in inlines:
        l = l.strip()  # remove newlines
        x = l.split("|")
        if len(x) == 2:
            orders[int(x[1])].add(int(x[0]))
        elif len(l) == 0:
            continue  # skip empty line
        else:
            x = list(map(int, l.split(",")))
            res, p1 = processline(orders, x)
            if p1:
                res1 += res
            else:
                res2 += res
    return str(res1), str(res2)
