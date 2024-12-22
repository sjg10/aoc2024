from collections import defaultdict


def evolve(num):
    num = (num ^ (num * 64)) % 16777216
    num = (num ^ (num // 32)) % 16777216
    return (num ^ (num * 2048)) % 16777216


def run(inlines):
    p1 = 0
    secrets = list(map(int, inlines))
    changes = defaultdict(dict)
    recentchanges = [[] for _ in range(len(secrets))]
    for i in range(2000):
        for j, x in enumerate(secrets):
            secrets[j] = evolve(x)
            todays_sale = secrets[j] % 10
            yesterdays_sale = x % 10
            recentchanges[j].append(todays_sale - yesterdays_sale)
            if i > 2:
                t = tuple(recentchanges[j])
                if j not in changes[t]:
                    changes[t][j] = todays_sale
                recentchanges[j].pop(0)
    p1 = sum(secrets)
    p2 = max(sum(changes[s][i] for i in changes[s]) for s in changes)
    return p1, p2
