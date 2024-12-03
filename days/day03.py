import re


def run(inlines):
    """
    Use regex to search for mul, do, don't accordingly
    """
    res1 = 0
    res2 = 0
    p2on = True
    for l in inlines:
        x = re.findall("(mul\\((\d*),(\d*)\\))|(do\(\\))|(don't\\(\\))", l)
        for m in x:
            if m[0]:
                # mul
                mul = int(m[1]) * int(m[2])
                res1 += mul
                if p2on:
                    res2 += mul
            elif m[3]:
                # do
                p2on = True
            elif m[4]:
                # dont
                p2on = False
    return str(res1), str(res2)
