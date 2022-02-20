from __future__ import annotations
from typing import TypeVar, Generic, Optional
from src.basic.meta_singleton import MetaSingleton  # type: ignore
from src.basic.suspension import Suspension  # type: ignore
from src.basic.comparable import Comparable  # type: ignore


CT = TypeVar('CT', bound=Comparable)


class LazyPairingHeap(Generic[CT], metaclass=MetaSingleton):
    value: CT
    heap: LazyPairingHeap[CT]
    suspheap: Suspension[LazyPairingHeap[CT]]

    def __init__(self, value: Optional[CT] = None,
                 heap: Optional[LazyPairingHeap[CT]] = None,
                 suspheap: Optional[Suspension[LazyPairingHeap[CT]]] = None
                 ) -> None:
        if value is not None:
            self.value = value
        if heap is not None:
            self.heap = heap
        if suspheap is not None:
            self.suspheap = suspheap

    def __bool__(self) -> bool:
        return self is not LazyPairingHeap()

    @staticmethod
    def _merge(hl: LazyPairingHeap[CT],
               hr: LazyPairingHeap[CT]) -> LazyPairingHeap[CT]:
        if not hl:
            return hr
        elif not hr:
            return hl
        elif hl.value <= hr.value:
            return LazyPairingHeap._link(hl, hr)
        return LazyPairingHeap._link(hr, hl)

    @staticmethod
    def _link(hl: LazyPairingHeap[CT],
              hr: LazyPairingHeap[CT]) -> LazyPairingHeap[CT]:
        if not hl.heap:
            return LazyPairingHeap(hl.value, hr, hl.suspheap)
        susp = Suspension(
            lambda: LazyPairingHeap._merge(LazyPairingHeap._merge(hr, hl.heap),
                                           hl.suspheap.force())
        )
        return LazyPairingHeap(hl.value, LazyPairingHeap(), susp)

    def insert(self, value: CT) -> LazyPairingHeap[CT]:
        susp = Suspension(lambda: LazyPairingHeap())
        new = LazyPairingHeap[CT](value, LazyPairingHeap(), susp)
        return LazyPairingHeap._merge(new, self)

    def find_min(self) -> CT:
        if not self:
            raise IndexError("find from empty heap")
        return self.value

    def delete_min(self) -> LazyPairingHeap[CT]:
        if not self:
            raise IndexError("delete from empty heap")
        return LazyPairingHeap._merge(self.heap, self.suspheap.force())
