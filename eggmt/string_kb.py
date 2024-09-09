def subseq(s, t):
    """Return index when s is a subsequence of t, None otherwise"""
    for i in range(len(t) - len(s) + 1):
        if s == t[i : i + len(s)]:
            return i
    return None


def replace(s, lhs, rhs):
    """"""
    i = subseq(lhs, s)
    if i is not None:
        return s[:i] + rhs + s[i + len(lhs) :]
    else:
        return s


def rewrite(s, R, exclude=-1):
    # exclude is useful for simplifying a rule
    while True:
        s0 = s
        for i, (lhs, rhs) in enumerate(R):
            if i != exclude:
                s = replace(s, lhs, rhs)
        if s == s0:
            return s


def shortlex(s, t):
    """order by length, then tie break by contents lex"""
    if len(s) < len(t):
        return t, s
    elif len(s) > len(t):
        return s, t
    elif s < t:
        return t, s
    elif s > t:
        return s, t
    else:
        assert False


def overlaps(s, t):
    """critical pairs https://en.wikipedia.org/wiki/Critical_pair_(term_rewriting)"""
    # make len(t) >= len(s)
    if len(t) < len(s):
        s, t = t, s
    if subseq(s, t) is not None:
        yield t
    # iterate over possible overlap sizes 1 to the len(s) at edges
    for osize in range(1, len(s)):
        if t[-osize:] == s[:osize]:
            yield t + s[osize:]
        if s[-osize:] == t[:osize]:
            yield s + t[osize:]


def deduce(R):
    """deduce all possible critical pairs from R"""
    for i, (lhs, rhs) in enumerate(R):
        for j in range(i):
            lhs1, rhs1 = R[j]
            for o in overlaps(lhs1, lhs):
                x, y = rewrite(o, [(lhs1, rhs1)]), rewrite(o, [(lhs, rhs)])
                if x != y:
                    yield x, y


def KB(E):
    E = E.copy()
    R = []
    done = False
    while not done:
        done = True
        E.extend(deduce(R))
        while E:
            lhs, rhs = E.pop()
            lhs, rhs = rewrite(lhs, R), rewrite(rhs, R)
            if lhs != rhs:
                done = False
                lhs, rhs = shortlex(lhs, rhs)
                R.append((lhs, rhs))

    return R


def simplify(R):
    Rnew = []
    E = []
    for i, (lhs, rhs) in enumerate(R):
        # lhs = reduce(Rnew)
        lhs1 = rewrite(
            lhs, R, exclude=i
        )  # L-simplify. nebulous correctness. I might be playing it both ways here. I keep around the old R even though I should have moved it to E?
        rhs1 = rewrite(rhs, R)  # R-simplify
        if lhs1 == lhs:
            Rnew.append((lhs, rhs1))
        elif lhs1 != rhs1:
            E.append((lhs1, rhs1))
    return E, Rnew
