from dataclasses import dataclass
from typing import NewType, NamedTuple


@dataclass
class FuncDeclRef:
    name: str
    ctx: object  # egraph variant

    def __call__(self, *args):
        pass


@dataclass
class ExprRef:  # Term
    decl: FuncDeclRef
    args: tuple[ExprRef, ...]


class Term(NamedTuple):
    head: str
    args: tuple["Term", ...]
