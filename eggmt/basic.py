from dataclasses import dataclass
import itertools
from typing import NewType, NamedTuple

EId = NewType("EId", int)


class ENode(NamedTuple):
    head: str
    args: tuple[EId, ...]


class Term(NamedTuple):
    head: str
    args: tuple["Term", ...]

    def children(self):
        return self.args


@dataclass
class FuncDeclRef:
    name: str
    ctx: object  # egraph variant

    def __call__(self, *args):
        return Term(self.name, args)

    def __getitem__(self, key):
        # creating lookup
        return Term(self.name, key)

    def __setitem__(self, key, value):
        # creating lookup and set
        pass


def Function(name, ctx=None):
    return FuncDeclRef(name, ctx)


@dataclass
class EGraph:
    enodes: dict[ENode, EId]
    uf: list[EId]

    def __init__(self):
        self.enodes = {}
        self.uf = []

    def makeset(self) -> EId:
        """Create a new equivalence class"""
        x = len(self.uf)
        self.uf.append(x)
        return x

    def find(self, x: EId) -> EId:
        """Get canonical EId"""
        while x != self.uf[x]:
            x = self.uf[x]
        return x

    def union(self, x: EId, y: EId) -> EId:
        x = self.find(x)
        y = self.find(y)
        if x != y:
            self.uf[x] = y
        return y

    def rebuild(self):
        while True:
            newenodes = {}
            for k, v in self.enodes.items():
                (head, args) = k
                newk = (head, tuple(self.find(a) for a in args))
                v1 = self.enodes.get(newk)
                if v1 is not None:
                    # congruence
                    self.union(v, v1)
                newenodes[newk] = self.find(v)
            if newenodes == self.enodes:
                break
            self.enodes = newenodes

    def add_term(self, t: Term) -> EId:
        head, args = t
        args = tuple(self.add_term(arg) for arg in args)
        v = self.enodes.get((head, args))
        if v is None:
            v = self.makeset()
            self.enodes[ENode(head, tuple(args))] = v
        return v

    def check_term(self, t: Term) -> bool:
        head, *args = t
        args = all(self.check_term(arg) for arg in args)
        return self.enodes.get(ENode(head, args))

    def rw(self, n: int, f):
        """
        Bottom up ematching. `n` is the number of pattern variables. `f` should return a pair of terms, a left hand side and right hand side.
        """
        ids = {self.find(x) for x in self.uf}
        for i in itertools.product(ids, repeat=n):
            lhs, rhs = f(*i)
            if self.check_term(lhs):
                self.union(self.add_term(lhs), self.add_term(rhs))

    def extract(self, e: EId) -> Term:
        # dynamic program cost
        cost = [float("inf")] * len(self.uf)
        best = [None] * len(self.uf)
        done = False
        while not done:
            done = True
            for enode, eid in self.enodes.items():
                head, args = enode
                print(enode, eid)
                enode_cost = 1 + sum(cost[a] for a in args)
                print(cost[eid], enode_cost)
                print(cost[eid] < enode_cost)
                if enode_cost < cost[eid]:
                    done = False
                    cost[eid] = enode_cost
                    best[eid] = enode
        print(self)
        print(best)
        print(cost)

        def _extract(e: EId) -> Term:
            head, args = best[e]
            return Term(head, tuple(_extract(a) for a in args))

        return _extract(e)
