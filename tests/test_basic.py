from eggmt.basic import EGraph, Term, EId


def test_basic():
    E = EGraph()
    term_a = Term("a", ())
    f = lambda x: Term("f", (x,))
    fa = E.add_term(f(term_a))
    a = E.add_term(term_a)
    assert isinstance(fa, int)
    assert a != fa
    g = lambda x: Term("g", (x,))

    assert not E.check_term(g(a))
    assert not E.check_term(f(f(a)))
    E.union(a, fa)
    assert E.find(fa) == E.find(a)
    E.rebuild()
    assert len(set(E.enodes.values())) == 1
    # assert E.check_term((ENode("f", (ENode("f", ("a",))),))
    assert E.find(fa) == E.find(a)
    E = EGraph()
    fa = E.add_term(f(term_a))
    assert len(E.uf) == 2
    a = E.add_term(term_a)
    E.union(a, fa)
    E.rebuild()
    assert E.extract(fa) == Term("a", ())
