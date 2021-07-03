from src.basic.list_stack import ListStack
from src.basic.suspension import Suspension


class PhysicistsQueue:
    def __init__(self, w=None, fsize=0, f=None, rsize=0, r=None):
        self.working = w if w is not None else ListStack()
        self.fsize = fsize
        self.f = f if f is not None else Suspension(lambda: ListStack())
        self.rsize = rsize
        self.r = r if r is not None else ListStack()

    def __bool__(self):
        return self.fsize != 0

    def _checkw(self):
        if not self.working:
            return PhysicistsQueue(self.f.force(), self.fsize, self.f,
                                   self.rsize, self.r)
        else:
            return self

    def _check(self):
        if self.rsize <= self.fsize:
            return self._checkw()
        f = self.f.force()
        susp = Suspension(lambda: f.concat(self.r.reverse()))
        return PhysicistsQueue(f, self.fsize + self.rsize, susp,
                               0, ListStack())._checkw()

    def snoc(self, value):
        return PhysicistsQueue(self.working, self.fsize, self.f,
                               self.rsize + 1, self.r.cons(value))._check()

    def head(self):
        if not self.working:
            raise IndexError("head from empty queue")
        return self.working.head()

    def tail(self):
        if not self.working:
            raise IndexError("tail from empty queue")
        susp = Suspension(lambda: self.f.force().tail())
        return PhysicistsQueue(self.working.tail(), self.fsize - 1, susp,
                               self.rsize, self.r)._check()
