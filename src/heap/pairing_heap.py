from src.basic.meta_singleton import MetaSingleton
from src.basic.list_stack import ListStack


class PairingHeap(metaclass=MetaSingleton):
    def __init__(self, value=None, heaplist=ListStack()):
        self.value = value
        self.heaplist = heaplist

    def __bool__(self):
        return self is not PairingHeap()

    @staticmethod
    def _merge(hl, hr):
        if not hl:
            return hr
        elif not hr:
            return hl
        elif hl.value <= hr.value:
            return PairingHeap(hl.value, hl.heaplist.cons(hr))
        return PairingHeap(hr.value, hr.heaplist.cons(hl))

    @staticmethod
    def _merge_pairs(heaplist):
        if not heaplist:
            return PairingHeap()
        elif not heaplist.tail():
            return heaplist.head()
        h1, heaplist = heaplist.head(), heaplist.tail()
        h2, heaplist = heaplist.head(), heaplist.tail()
        return PairingHeap._merge(PairingHeap._merge(h1, h2),
                                  PairingHeap._merge_pairs(heaplist))

    def insert(self, value):
        new = PairingHeap(value, ListStack())
        return PairingHeap._merge(new, self)

    def find_min(self):
        if not self:
            raise IndexError("find from empty heap")
        return self.value

    def delete_min(self):
        if not self:
            raise IndexError("delete from empty heap")
        return PairingHeap._merge_pairs(self.heaplist)
