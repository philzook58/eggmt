import z3
import itertools
from collections import defaultdict


class Z3Graph:
    def __init__(self):
        self.solver = z3.Solver()
        self.terms = defaultdict(set)  # keyed by sort
        self.uf = {}

    def find(self, e: z3.ExprRef) -> z3.ExprRef:
        while not self.uf[e].eq(e):
            e = self.uf[e]
        return e

    def add_term(self, e: z3.ExprRef) -> z3.ExprRef:
        if e not in self.uf:
            self.uf[e] = e
            self.terms[e.sort()].add(e)
            if z3.is_app(e):
                for c in e.children():
                    self.add_term(c)
            return e
        else:
            return self.find(e)

    def union(self, e1: z3.ExprRef, e2: z3.ExprRef) -> z3.ExprRef:
        # TODO: should we add_term in union?
        e1 = self.find(e1)
        e2 = self.find(e2)
        if e1.eq(e2):
            return e1
        else:
            self.solver.add(
                e1 == e2
            )  # assert_and_track? unsat core gives a form of proof.
            self.uf[e1] = e2
            return e2

    def rebuild(self):
        done = False
        while not done:
            done = True
            for t, s in self.uf.items():
                f = t.decl()
                f1 = self.add_term(f(*[self.find(c) for c in t.children()]))
                if not self.find(f1).eq(s):
                    done = False
                    self.union(f1, s)
        self.terms = {
            sort: {self.find(t) for t in ts} for sort, ts in self.terms.items()
        }

    def rw(self, sorts: list[z3.SortRef], f):
        for terms in itertools.product(*[self.terms[s] for s in sorts]):
            lhs, rhs = f(*terms)
            lhs = self.find(lhs)
            if self.find(lhs) in self.terms:
                rhs = self.add_term(rhs)
                self.union(lhs, rhs)

    def search(self, sorts: list[z3.SortRef]):
        """Search over terms"""
        yield from itertools.product(*[self.terms[s] for s in sorts])
