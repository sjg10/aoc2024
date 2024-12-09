def calc_score(fileID, startpos, count):
    score = 0
    for i in range(startpos, startpos + count):
        score += fileID * i
    return score


def part1(l):
    res = 0
    lptr = 0  # ptr in string
    rptr = len(l) - 1
    lidx = 0  # block index in filesystem
    l2 = l.copy()
    lid = 0  # fileid of file at lptr
    rid = len(l) // 2

    # Move the lptr to the first free space
    # move to the free space on the left
    lidx += l2[lptr]
    lptr += 1

    while lptr < rptr:  # Read from left and right, meet in middle
        # move the right file into the space
        moving = l2[rptr] if l2[rptr] <= l2[lptr] else l2[lptr]
        res += calc_score(rid, lidx, moving)
        l2[rptr] -= moving
        l2[lptr] -= moving
        lidx += moving
        if l2[lptr] == 0:
            # Move lid
            lptr += 1
            lid += 1
            if lid == rid:
                # In the middle of a block on both sides at the end:
                res += calc_score(lid, lidx, l2[rptr])
                break
            # Get the next file:
            res += calc_score(lid, lidx, l2[lptr])
            # And move lid to the next empty block
            lidx += l2[lptr]
            lptr += 1
        if l2[rptr] == 0:
            # Move rid to next non-empty block
            rptr -= 2
            rid -= 1
    return res


def part2(l):
    # Original
    poss = [0]
    for p in l:
        poss.append(poss[-1] + p)

    # For editing
    l2 = l.copy()

    res = 0

    for ridx in range(len(l) - 1, -1, -2):
        for lidx in range(1, ridx, 2):
            if l2[lidx] >= l[ridx]:
                l2[lidx] -= l[ridx]
                res += calc_score(ridx // 2, poss[lidx], l[ridx])
                poss[lidx] += l[ridx]
                break
        else:  # didnt move
            res += calc_score(ridx // 2, poss[ridx], l[ridx])
    return res


def run(inlines):
    l = [int(x) for x in next(inlines).strip()]
    assert len(l) % 2  # assume last entry is a file and not space
    return part1(l), part2(l)
