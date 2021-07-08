from src.basic.meta_singleton import MetaSingleton
from src.basic.list_stack import ListStack
from src.basic.suspension import Suspension


class LazyPairingHeap(metaclass=MetaSingleton):
    def __init__(self, value=None, heap=None, suspheap=None):
        self.value = value
        self.heap = heap
        self.suspheap = suspheap

    def __bool__(self):
        return self is not LazyPairingHeap()

    @staticmethod
    def _merge(hl, hr):
        if not hl:
            return hr
        elif not hr:
            return hl
        elif hl.value <= hr.value:
            return LazyPairingHeap._link(hl, hr)
        return LazyPairingHeap._link(hr, hl)

    @staticmethod
    def _link(hl, hr):
        if not hl.heap:
            return LazyPairingHeap(hl.value, hr, hl.suspheap)
        susp = Suspension(
            lambda: LazyPairingHeap._merge(LazyPairingHeap._merge(hr, hl.heap),
                                           hl.suspheap.force())
        )
        return LazyPairingHeap(hl.value, LazyPairingHeap(), susp)

    def insert(self, value):
        susp = Suspension(lambda: LazyPairingHeap())
        new = LazyPairingHeap(value, LazyPairingHeap(), susp)
        return LazyPairingHeap._merge(new, self)

    def find_min(self):
        if not self:
            raise IndexError("find from empty heap")
        return self.value

    def delete_min(self):
        if not self:
            raise IndexError("delete from empty heap")
        return LazyPairingHeap._merge(self.heap, self.suspheap.force())
