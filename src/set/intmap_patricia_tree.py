from __future__ import annotations
from typing import TypeVar, Generic, Optional, Union


VT = TypeVar('VT')


class Leaf(Generic[VT]):
    k: int
    elem: VT

    def __init__(self, k: int, elem: VT) -> None:
        self.k = k
        self.elem = elem


Tree = Union["Branch[VT]", Leaf[VT]]


class Branch(Generic[VT]):
    prefix: int
    mask: int
    tl: Tree[VT]
    tr: Tree[VT]

    def __init__(self, prefix: int, mask: int,
                 tl: Tree[VT], tr: Tree[VT]) -> None:
        self.prefix = prefix
        self.mask = mask
        self.tl = tl
        self.tr = tr

    @staticmethod
    def new(prefix: int, mask: int,
            tl: Optional[Tree[VT]], tr: Optional[Tree[VT]]) -> Tree[VT]:
        if tl is not None and tr is not None:
            return Branch(prefix, mask, tl, tr)
        elif tl is None and tr is not None:
            return tr
        elif tr is None and tl is not None:
            return tl
        else:
            raise ValueError("tl or tl must not be None")

    def match_prefix(self, k: int) -> bool:
        return k & (self.mask - 1) == self.prefix

    def zerobit(self, k: int) -> bool:
        return k & self.mask == 0


class IntMapPatriciaTree(Generic[VT]):
    root: Optional[Tree[VT]]

    def __init__(self, root: Optional[Tree[VT]] = None) -> None:
        self.root = root

    def __bool__(self) -> bool:
        return self.root is not None

    def _branching_bit(self, p0: int, p1: int) -> int:
        x = p0 ^ p1
        return x & -x

    def _join(self, p0: int, t0: Tree[VT], p1: int, t1: Tree[VT]) -> Tree[VT]:
        m = self._branching_bit(p0, p1)
        if p0 & m == 0:
            return Branch.new(p0 & (m - 1), m, t0, t1)
        else:
            return Branch.new(p0 & (m - 1), m, t1, t0)

    def lookup(self, k: int) -> Optional[VT]:
        def lkup(node: Optional[Tree[VT]]) -> Optional[VT]:
            if node is None:
                return None
            elif isinstance(node, Leaf):
                if k == node.k:
                    return node.elem
                else:
                    return None
            else:
                if not node.match_prefix(k):
                    return None
                if node.zerobit(k):
                    return lkup(node.tl)
                return lkup(node.tr)

        return lkup(self.root)

    def insert(self, k: int, elem: VT) -> IntMapPatriciaTree[VT]:
        def ins(node: Optional[Tree[VT]]) -> Tree[VT]:
            if node is None:
                return Leaf(k, elem)
            elif isinstance(node, Leaf):
                if k == node.k:
                    return Leaf(k, elem)
                else:
                    return self._join(k, Leaf(k, elem), node.k, node)
            else:
                if not node.match_prefix(k):
                    return self._join(k, Leaf(k, elem), node.prefix, node)
                if node.zerobit(k):
                    return Branch.new(node.prefix, node.mask,
                                      ins(node.tl), node.tr)
                return Branch.new(node.prefix, node.mask,
                                  node.tl, ins(node.tr))

        return IntMapPatriciaTree(ins(self.root))
