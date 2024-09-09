from dataclasses import dataclass
import itertools

EId = int
ENode = tuple[str, tuple[EId, ...]]
Term = tuple[str, "Term", ...]


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
        head, *args = t
        args = tuple(self.add_term(arg) for arg in args)
        v = self.enodes.get((head, args))
        if v is None:
            v = self.makeset()
            self.enodes[(head, tuple(args))] = v
        return v

    def check_term(self, t: Term) -> bool:
        """
        TODO
        head, *args = t
        if all(self.check_term(arg) for arg in args):
            return self.enodes.get((head, tuple(args)))
        """
        assert False

    def rw(self, n: int, f):
        """
        Bottom up ematching. `n` is the number of pattern variables. `f` should return a pair of terms, a left hand side and right hand side.
        """
        ids = {self.find(x) for x in self.uf}
        for i in itertools.product(ids, repeat=n):
            lhs, rhs = f(*i)
            if self.check_term(lhs):
                self.union(self.add_term(lhs), self.add_term(rhs))
