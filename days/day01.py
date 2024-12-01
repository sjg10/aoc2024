from collections import defaultdict
from bisect import insort


def parse(inlines):
    """
    Parse the incoming data into a sorted left list, right list and summary map of right.
    """
    l = []
    r = []
    summary = defaultdict(int)
    for line in inlines:
        sl, sr = map(int, line.split())
        insort(l, sl)
        insort(r, sr)
        summary[sr] += 1
    return l, r, summary


def summarise(l, r, summary):
    """
    Calculate the score for both parts
    """
    res1 = 0
    res2 = 0
    for i in range(len(l)):
        res1 += abs(l[i] - r[i])
        res2 += l[i] * summary[l[i]]
    return str(res1), str(res2)


def run(inlines):
    l, r, summary = parse(inlines)
    return summarise(l, r, summary)
