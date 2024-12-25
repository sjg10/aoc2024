from itertools import product


def get_key_lock(inlines):
    item = [0, 0, 0, 0, 0]
    l = next(inlines)
    lock = l[0] == "#"
    for i in range(5):
        l = next(inlines)
        for j in range(5):
            if l[j] == "#":
                item[j] += 1
    l = next(inlines)
    try:
        l = next(inlines)
    except StopIteration:
        return True, lock, item
    return False, lock, item


def fits(lock, key):
    return all(lock[i] + key[i] <= 5 for i in range(5))


def run(inlines):
    stop = False
    locks = []
    keys = []
    while not stop:
        stop, lock, item = get_key_lock(inlines)
        if lock:
            locks.append(item)
        else:
            keys.append(item)
    p1 = sum(1 for lock, key in product(locks, keys) if fits(lock, key))
    return p1, None
