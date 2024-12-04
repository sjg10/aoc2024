import re


def skp(n):
    """
    Regex string to skip n characters
    """
    return f"[A-Z\\n]{{{n}}}"


def run(inlines):
    txt = "".join(inlines)
    r = txt.index("\n")
    p1 = [
        f"(?=XMAS)",
        f"(?=SAMX)",
        f"(?=X{skp(r)}M{skp(r)}A{skp(r)}S)",
        f"(?=S{skp(r)}A{skp(r)}M{skp(r)}X)",
        f"(?=X{skp(r-1)}M{skp(r-1)}A{skp(r-1)}S)",
        f"(?=X{skp(r+1)}M{skp(r+1)}A{skp(r+1)}S)",
        f"(?=S{skp(r-1)}A{skp(r-1)}M{skp(r-1)}X)",
        f"(?=S{skp(r+1)}A{skp(r+1)}M{skp(r+1)}X)",
    ]
    res1 = sum(map(lambda p: len(re.findall(p, txt)), p1))
    p2 = [
        f"(?=S[A-Z]S{skp(r-1)}A{skp(r-1)}M[A-Z]M)",
        f"(?=S[A-Z]M{skp(r-1)}A{skp(r-1)}S[A-Z]M)",
        f"(?=M[A-Z]S{skp(r-1)}A{skp(r-1)}M[A-Z]S)",
        f"(?=M[A-Z]M{skp(r-1)}A{skp(r-1)}S[A-Z]S)",
    ]
    res2 = sum(map(lambda p: len(re.findall(p, txt)), p2))
    return str(res1), str(res2)
