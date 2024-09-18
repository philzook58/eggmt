from eggmt.aegraph import AEGraph


def test_aegraph():
    E = AEGraph()
    one = E.const(1)
    two = E.const(2)
    E
    a = E.var("a")
    E.union(a, one)
    assert a == E.add_term(("var", "a"))
    assert one == E.add_term(("const", 1))
    print(E)
    mulaone = E.mul(a, one)
    print(mulaone)
    print(E)
    E.find(E.add_term(("mul", ("$eid", a), ("$eid", one)))) == mulaone
    E.mul(one, one)
    E.check()
    divnode = E.div(E.mul(a, two), two)
    assert E.find(divnode) == E.find(a)
