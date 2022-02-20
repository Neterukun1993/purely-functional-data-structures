from __future__ import annotations
from typing import TypeVar, Generic, Optional
from src.basic.meta_singleton import MetaSingleton  # type: ignore
from src.basic.comparable import Comparable  # type: ignore


CT = TypeVar('CT', bound=Comparable)


class LeftistHeap(Generic[CT], metaclass=MetaSingleton):
    rank: int
    value: CT
    a: LeftistHeap[CT]
    b: LeftistHeap[CT]

    def __init__(self, rank: int = 0, value: Optional[CT] = None,
                 a: Optional[LeftistHeap[CT]] = None,
                 b: Optional[LeftistHeap[CT]] = None) -> None:
        self.rank = rank
        if value is not None:
            self.value = value
        if a is not None:
            self.a = a
        if b is not None:
            self.b = b

    def __bool__(self) -> bool:
        return self is not LeftistHeap()

    @staticmethod
    def _make(value: CT, a: LeftistHeap[CT],
              b: LeftistHeap[CT]) -> LeftistHeap[CT]:
        if a.rank >= b.rank:
            a, b = b, a
        return LeftistHeap(a.rank + 1, value, b, a)

    @staticmethod
    def merge(hl: LeftistHeap[CT], hr: LeftistHeap[CT]) -> LeftistHeap[CT]:
        if not hl:
            return hr
        elif not hr:
            return hl
        elif hl.value <= hr.value:
            return LeftistHeap._make(hl.value, hl.a,
                                     LeftistHeap.merge(hl.b, hr))
        else:
            return LeftistHeap._make(hr.value, hr.a,
                                     LeftistHeap.merge(hl, hr.b))

    def insert(self, value: CT) -> LeftistHeap[CT]:
        new: LeftistHeap[CT] = LeftistHeap(1, value,
                                           LeftistHeap(), LeftistHeap())
        return LeftistHeap.merge(new, self)

    def find_min(self) -> CT:
        if not self:
            raise IndexError("find from empty heap")
        return self.value

    def delete_min(self) -> LeftistHeap[CT]:
        if not self:
            raise IndexError("delete from empty heap")
        return self.merge(self.a, self.b)
