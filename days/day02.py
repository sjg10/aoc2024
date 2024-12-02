def check(x, y, increasing):
    """
    Check if two values are safe, given an increasing or not sequence
    """
    if not 1 <= abs(y - x) <= 3:
        return False
    elif increasing and y < x:
        return False
    elif not increasing and y > x:
        return False
    return True


def get_safe(ls):
    """
    Checks if ls list is safe, returns safe, first_unsafe_index
    """
    increasing = ls[2] > ls[1]
    for i in range(1, len(ls)):
        if not check(ls[i - 1], ls[i], increasing):
            break
    else:
        return True, None
    return False, i


def run(inlines):
    res1 = 0
    res2 = 0
    for l in inlines:
        ls = list(map(int, l.split()))
        inc, pos = get_safe(ls)
        if inc:
            res1 += 1
            res2 += 1
        else:
            for j in [pos - 1, pos, pos + 1]:
                if get_safe(ls[0:j] + ls[j + 1 :])[0]:
                    res2 += 1
                    break
    return str(res1), str(res2)
