from src.basic.list_stack import ListStack
from src.basic.suspension import Suspension
from src.queue.real_time_queue import RealTimeQueue


class BootstrappedQueue:
    def __init__(self, fmsize=0, f=None, m=None, rsize=0, r=None):
        self.fmsize = fmsize
        self.f = ListStack() if f is None else f
        self.m = RealTimeQueue() if m is None else m
        self.rsize = rsize
        self.r = ListStack() if r is None else r

    def __bool__(self):
        return self.fmsize != 0

    def _check_q(self):
        if self.fmsize >= self.rsize:
            return self._check_f()
        else:
            susp = Suspension(lambda: self.r.reverse())
            return BootstrappedQueue(self.fmsize + self.rsize, self.f,
                                     self.m.snoc(susp), 0,
                                     ListStack())._check_f()

    def _check_f(self):
        if not self.f and not self.m:
            return BootstrappedQueue()
        elif not self.f:
            return BootstrappedQueue(self.fmsize, self.m.head().force(),
                                     self.m.tail(), self.rsize, self.r)
        else:
            return self

    def snoc(self, value):
        return BootstrappedQueue(self.fmsize, self.f, self.m, self.rsize + 1,
                                 self.r.cons(value))._check_q()

    def head(self):
        if not self:
            raise IndexError("head from empty queue")
        return self.f.head()

    def tail(self):
        if not self:
            raise IndexError("tail from empty queue")
        return BootstrappedQueue(self.fmsize - 1, self.f.tail(), self.m,
                                 self.rsize, self.r)._check_q()
