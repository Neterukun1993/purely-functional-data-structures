from src.basic.meta_singleton import MetaSingleton
from src.basic.suspension import Suspension
from src.queue.real_time_queue import RealTimeQueue


class CatenableList(metaclass=MetaSingleton):
    def __init__(self, _head=None, q=None):
        self._head = _head
        self.q = RealTimeQueue() if q is None else q

    def __bool__(self):
        return self is not CatenableList()

    def _link(self, susp):
        return CatenableList(self._head, self.q.snoc(susp))

    @staticmethod
    def _link_all(q):
        t = q.head().force()
        q_tail = q.tail()
        if q_tail:
            susp = Suspension(lambda: CatenableList._link_all(q_tail))
            return t._link(susp)
        else:
            return t

    def concat(self, other):
        if not other:
            return self
        if not self:
            return other
        return self._link(Suspension(other))

    def cons(self, value):
        return CatenableList(value, RealTimeQueue()).concat(self)

    def snoc(self, value):
        return self.concat(CatenableList(value, RealTimeQueue()))

    def head(self):
        if not self:
            raise IndexError("head from empty list")
        return self._head

    def tail(self):
        if not self:
            raise IndexError("tail from empty list")
        if self.q:
            return CatenableList._link_all(self.q)
        return CatenableList()
