from dataclasses import dataclass, field
from typing import Optional, NewType, Iterable
import itertools

EId = NewType("EId", int)


@dataclass(frozen=True)
class ELit:
    value: object


@dataclass(frozen=True)
class Enode:
    name: str
    args: tuple[EId, ...]


@dataclass
class AEGraph:
    uf: list[EId] = field(default_factory=list)
    unodes: list[Optional[tuple[EId, EId]]] = field(default_factory=list)
    enodes: list[Optional[Enode | ELit]] = field(default_factory=list)
    hashcons: dict[Enode | ELit, EId] = field(default_factory=dict)

    def makeset(self) -> EId:
        z = len(self.uf)
        self.uf.append(z)
        self.unodes.append(None)  # or really it might hold an actual thing.
        self.enodes.append(None)
        return EId(z)

    def find(self, x: EId) -> EId:
        while self.uf[x] != x:
            x = self.uf[x]
        return x

    def union(self, x: EId, y: EId) -> EId:
        assert isinstance(x, int) and isinstance(y, int)
        x = self.find(x)
        y = self.find(y)
        if x != y:
            z = self.makeset()
            self.uf[x] = z
            self.uf[y] = z
            self.unodes[z] = (x, y)
            return z
        else:
            return x

    def enum(self, x: EId) -> Iterable[EId]:
        t = self.unodes[x]
        match t:
            case None:
                yield x
            case (l, r):
                yield from self.enum(l)
                yield from self.enum(r)
            case _:
                raise ValueError("Invalid value", x)

    def add_enode(self, enode: (Enode | ELit)) -> EId:
        # should I call find on the enode args here?
        eid = self.hashcons.get(enode)
        if eid is not None:
            return eid
        eid = self.makeset()
        self.enodes[eid] = enode
        self.hashcons[enode] = eid
        return eid

    def add_term(self, term) -> EId:
        if isinstance(term, tuple):
            if term[0] == "$eid":
                return term[1]
            else:
                name, *args = term
                args = tuple(self.add_term(arg) for arg in args)
                return self.add_enode(Enode(name, args))
        else:
            return self.add_enode(ELit(term))

    def term_view(self, eid: EId, depth: int):
        assert depth >= 0
        if depth == 0:  # don't expand and leave it as special unexpanded term
            yield ("$eid", eid)
        else:
            for eid1 in self.enum(eid):
                enode = self.enodes[eid1]
                if isinstance(enode, ELit):
                    yield enode.value
                elif isinstance(enode, Enode):
                    for args in itertools.product(
                        *[self.term_view(arg, depth - 1) for arg in enode.args]
                    ):
                        yield (enode.name, *args)

    def check(self):
        # sanity check properties
        for enode, unode in zip(self.enodes, self.unodes):
            assert (unode is None) != (enode is None)
        for eid, unode in enumerate(self.unodes):
            assert unode is None or isinstance(unode, tuple)
        for eid, enode in enumerate(self.enodes):
            if enode is not None:
                assert isinstance(enode, Enode | ELit)
                assert self.hashcons[enode] == eid

    # theory specific smart constructors
    def const(self, x: int) -> EId:
        eid = self.add_term(("const", x))
        return eid

    def var(self, name: str) -> EId:
        eid = self.add_term(("var", name))
        return eid

    def mul(self, x: EId, y: EId) -> EId:
        eid = self.add_enode(Enode("mul", (x, y)))
        for t in self.term_view(eid, 3):
            match t:
                case ("mul", ("const", x), ("const", y)):
                    self.union(self.const(x * y), eid)
            match t:
                case ("mul", ("const", 0), b) | ("mul", b, ("const", 0)):
                    self.union(self.const(0), eid)
            match t:
                case ("mul", ("const", 1), b) | ("mul", b, ("const", 1)):
                    self.union(self.add_term(b), eid)
            match t:
                case ("mul", a, ("const", 2)):
                    self.union(self.lshift(self.add_term(a), self.const(1)), eid)
        return self.find(eid)

    def lshift(self, x: EId, y: EId) -> EId:
        eid = self.add_enode(Enode("lshift", (x, y)))
        for t in self.term_view(eid, 3):
            match t:
                case ("lshift", ("const", 0), b):
                    self.union(self.const(0), eid)
            match t:
                case ("lshift", a, ("const", 0)):
                    self.union(self.add_term(a), eid)
            match t:
                case ("lshift", ("const", x), ("const", y)):
                    self.union(self.const(x << y), eid)
        return self.find(eid)

    def div(self, x: EId, y: EId) -> EId:
        eid = self.add_enode(Enode("div", (x, y)))
        for t in self.term_view(eid, 4):
            match t:
                case ("div", ("mul", a, b), b1) if b == b1 and b != 0:
                    self.union(self.add_term(a), eid)
        return self.find(eid)
