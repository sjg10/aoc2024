from collections import defaultdict, Counter


def blink(s):
    s2 = defaultdict(int)
    for x in s:
        if x == 0:
            s2[1] += s[x]
        else:
            st = str(x)
            if len(st) % 2 == 0:
                s2[int(st[: len(st) // 2])] += s[x]
                s2[int(st[len(st) // 2 :])] += s[x]
            else:
                s2[x * 2024] += s[x]
    return s2


def run(inlines):
    s = Counter(map(int, next(inlines).split()))
    for n in range(25):
        s = blink(s)
    p1 = sum(s.values())
    for n in range(50):
        s = blink(s)
    p2 = sum(s.values())
    return p1, p2
