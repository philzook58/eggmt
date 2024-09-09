from eggmt.basic import EGraph


def test_basic():
    E = EGraph()
    fa = E.add_term(("f", ("a",)))
    a = E.add_term(("a",))
    assert a != fa
    assert not E.check_term(("g", ("a",)))
    assert not E.check_term(("f", ("f", ("a",))))
    E.union(a, fa)
    assert E.find(fa) == E.find(a)
    E.rebuild()
    assert len(set(E.enodes.values())) == 1
    assert E.check_term(("f", ("f", ("a",))))
    assert E.find(fa) == E.find(a)
