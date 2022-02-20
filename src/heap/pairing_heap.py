from __future__ import annotations
from typing import TypeVar, Generic, Optional
from src.basic.meta_singleton import MetaSingleton  # type: ignore
from src.basic.list_stack import ListStack  # type: ignore
from src.basic.comparable import Comparable  # type: ignore


CT = TypeVar('CT', bound=Comparable)


class PairingHeap(Generic[CT], metaclass=MetaSingleton):
    value: CT
    heaplist: ListStack[PairingHeap[CT]]

    def __init__(self,
                 value: Optional[CT] = None,
                 heaplist: Optional[ListStack[PairingHeap[CT]]]
                 = None) -> None:
        if value is not None:
            self.value = value
        self.heaplist = ListStack() if heaplist is None else heaplist

    def __bool__(self) -> bool:
        return self is not PairingHeap()

    @staticmethod
    def _merge(hl: PairingHeap[CT], hr: PairingHeap[CT]) -> PairingHeap[CT]:
        if not hl:
            return hr
        elif not hr:
            return hl
        elif hl.value <= hr.value:
            return PairingHeap(hl.value, hl.heaplist.cons(hr))
        return PairingHeap(hr.value, hr.heaplist.cons(hl))

    @staticmethod
    def _merge_pairs(heaplist: ListStack[PairingHeap[CT]]) -> PairingHeap[CT]:
        if not heaplist:
            return PairingHeap()
        elif not heaplist.tail():
            head: PairingHeap[CT] = heaplist.head()
            return head
        h1, heaplist = heaplist.head(), heaplist.tail()
        h2, heaplist = heaplist.head(), heaplist.tail()
        return PairingHeap._merge(PairingHeap._merge(h1, h2),
                                  PairingHeap._merge_pairs(heaplist))

    def insert(self, value: CT) -> PairingHeap[CT]:
        new: PairingHeap[CT] = PairingHeap(value, ListStack())
        return PairingHeap._merge(new, self)

    def find_min(self) -> CT:
        if not self:
            raise IndexError("find from empty heap")
        return self.value

    def delete_min(self) -> PairingHeap[CT]:
        if not self:
            raise IndexError("delete from empty heap")
        return PairingHeap._merge_pairs(self.heaplist)
