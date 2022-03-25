from __future__ import annotations
from typing import TypeVar, Generic, Optional, Tuple
from src.basic.meta_singleton import MetaSingleton  # type: ignore
from src.basic.comparable import Comparable  # type: ignore


CT = TypeVar('CT', bound=Comparable)


class SplayHeap(Generic[CT], metaclass=MetaSingleton):
    value: CT
    a: SplayHeap[CT]
    b: SplayHeap[CT]

    def __init__(self, value: Optional[CT] = None,
                 a: Optional[SplayHeap[CT]] = None,
                 b: Optional[SplayHeap[CT]] = None) -> None:
        if value is not None:
            self.value = value
        if a is not None:
            self.a = a
        if b is not None:
            self.b = b

    def __bool__(self) -> bool:
        return self is not SplayHeap()

    def partition(self, pivot: CT) -> Tuple[SplayHeap[CT], SplayHeap[CT]]:
        if not self:
            return SplayHeap(), SplayHeap()
        if self.value <= pivot:
            if not self.b:
                return self, SplayHeap()
            else:
                if self.b.value <= pivot:
                    small, big = self.b.b.partition(pivot)
                    return SplayHeap(self.b.value,
                                     SplayHeap(self.value, self.a, self.b.a),
                                     small), big
                else:
                    small, big = self.b.a.partition(pivot)
                    return (SplayHeap(self.value, self.a, small),
                            SplayHeap(self.b.value, big, self.b.b))
        else:
            if not self.a:
                return SplayHeap(), self
            else:
                if self.a.value <= pivot:
                    small, big = self.a.b.partition(pivot)
                    return (SplayHeap(self.a.value, self.a.a, small),
                            SplayHeap(self.value, big, self.b))
                else:
                    small, big = self.a.a.partition(pivot)
                    return small, SplayHeap(self.a.value, big,
                                            SplayHeap(self.value,
                                                      self.a.b, self.b))

    @staticmethod
    def merge(hl: SplayHeap[CT], hr: SplayHeap[CT]) -> SplayHeap[CT]:
        if not hl:
            return hr
        a, b = hr.partition(hl.value)
        return SplayHeap(hl.value,
                         SplayHeap.merge(a, hl.a),
                         SplayHeap.merge(b, hl.b))

    def insert(self, value: CT) -> SplayHeap[CT]:
        a, b = self.partition(value)
        return SplayHeap(value, a, b)

    def find_min(self) -> CT:
        if not self:
            raise IndexError("find from empty heap")
        if not self.a:
            return self.value
        return self.a.find_min()

    def delete_min(self) -> SplayHeap[CT]:
        if not self:
            raise IndexError("delete from empty heap")
        if not self.a:
            return self.b
        if not self.a.a:
            return SplayHeap(self.value, self.a.b, self.b)
        return SplayHeap(self.a.value,
                         self.a.a.delete_min(),
                         SplayHeap(self.value, self.a.b, self.b))
