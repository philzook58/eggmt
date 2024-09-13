import sympy as sp
from dataclasses import dataclass
import itertools


EClass = sp.Symbol
ENode = tuple[str, ...]


# helper functions to turn integers into sympy symbols
def sympy_eclass(n):
    return sp.symbols("e" + str(n))


def eclass_of_sympy(eclass):
    return int(eclass.name[1:])


# https://www.philipzucker.com/linear_grobner_egraph/


@dataclass
class EGraph:
    poly_eqs: list[sp.Expr]
    hashcons: dict[ENode, EClass]
    eclasses: list[EClass]

    def __init__(self):
        self.poly_eqs = []
        self.hashcons: dict[ENode, EClass] = {}
        self.eclasses = []

    def find(self, x: EClass) -> EClass:
        return sp.reduced(x, self.poly_eqs, self.eclasses)[1]

    def union(self, x: EClass, y: EClass) -> EClass:
        x = self.find(x)
        y = self.find(y)
        if x != y:
            self.poly_eqs.append(x - y)

    def makeset(self):
        x = sympy_eclass(len(self.eclasses))
        self.eclasses.append(x)
        return x

    def make(self, t: ENode) -> EClass:
        t1 = self.hashcons.get(t)
        if t1 == None:
            v = self.makeset()
            self.hashcons[t] = v
            return v
        else:
            return t1

    def rebuild(self):
        # simple naive dumb rebuild step. Could be optimized signifcantly
        while True:
            # rebuild "union find", buchberhe
            self.poly_eqs = list(sp.groebner(self.poly_eqs, *self.eclasses))

            # rebuild hashcons"
            newhashcons = {}
            for k, v in self.hashcons.items():
                (f, *args) = k
                args = map(self.find, args)  # normalize argument eclasses
                enode = (f, *args)
                eclass = self.hashcons.get(enode)
                if eclass != None:
                    self.union(v, eclass)
                newhashcons[enode] = self.find(v)
            if self.hashcons == newhashcons:  # reached fixed point
                return
            self.hashcons = newhashcons

    def add_term(self, t):
        if isinstance(t, sp.Expr):  # allow partial terms that contain eclasses
            return t
        f, *args = t
        args = map(self.add_term, args)
        return self.make_enode((f, *args))

    def check_term(self, t):
        if isinstance(t, sp.Expr):  # allow partial terms that contain eclasses
            return t
        f, *args = t
        map(self.check_term, args)
        return (f, *args)

    def make_enode(self, enode):
        eclass = self.hashcons.get(enode)
        if eclass == None:
            eclass = self.makeset()
            self.hashcons[enode] = eclass
        return eclass

    def rw(self, n, f):
        for eclasses in itertools.product(self.eclasses, repeat=n):
            lhs, rhs = f(*eclasses)
            # whatever
            lhs = self.add_term(lhs)
            rhs = self.add_term(rhs)
            self.union(lhs, rhs)


# TODO: There is a pure sympy version
