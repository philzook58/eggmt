from eggmt.z3graph import Z3Graph
import z3


def test_z3graph():
    E = Z3Graph()
    x = z3.Int("x")
    y = z3.Int("y")
    z = z3.Int("z")
    E.add_term(x + y)
    E.add_term(y + z)
    E.union(x + y, y + z)
    E.rebuild()
    assert len(E.terms) == 1
