from src.basic.meta_singleton import MetaSingleton
from src.basic.list_stack import ListStack
from src.basic.suspension import Suspension


class _BootstrappedQueue:
    def __init__(self, fmsize, f, m, rsize, r):
        self.fmsize = fmsize
        self.f = f
        self.m = m
        self.rsize = rsize
        self.r = r

    def __bool__(self):
        return True

    def _check_q(self):
        if self.fmsize >= self.rsize:
            return self._check_f()
        else:
            susp = Suspension(lambda: self.r.reverse())
            return _BootstrappedQueue(self.fmsize + self.rsize, self.f,
                                      self.m.snoc(susp), 0,
                                      ListStack())._check_f()

    def _check_f(self):
        if self.m is BootstrappedQueue() and not self.f:
            return BootstrappedQueue()
        if not self.f:
            return _BootstrappedQueue(self.fmsize, self.m.head().force(),
                                      self.m.tail(), self.rsize, self.r)
        return self

    def snoc(self, value):
        return _BootstrappedQueue(self.fmsize, self.f, self.m, self.rsize + 1,
                                  self.r.cons(value))._check_q()

    def head(self):
        return self.f.head()

    def tail(self):
        return _BootstrappedQueue(self.fmsize - 1, self.f.tail(), self.m,
                                  self.rsize, self.r)._check_q()


class BootstrappedQueue(metaclass=MetaSingleton):
    def __init__(self):
        self.fmsize = 0
        self.f = ListStack()
        self.m = self
        self.rsize = 0
        self.r = ListStack()

    def __bool__(self):
        return False

    def snoc(self, value):
        return _BootstrappedQueue(1, ListStack().cons(value), self,
                                  0, ListStack())

    def head(self):
        raise IndexError("head from empty queue")

    def tail(self):
        raise IndexError("tail from empty queue")
