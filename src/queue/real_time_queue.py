from src.basic.list_stack import ListStack
from src.basic.stream import Stream


class RealTimeQueue:
    def __init__(self, f=None, r=None, s=None):
        self.f = Stream() if f is None else f
        self.r = ListStack() if r is None else r
        self.s = Stream() if s is None else s

    def __bool__(self):
        return self.f is not Stream.Nil

    @staticmethod
    def _rotate(f, r, s):
        if not f:
            return s.cons(r.head())
        func = lambda: (f.head(), RealTimeQueue._rotate(f.tail(),
                                                        r.tail(),
                                                        s.cons(r.head())))
        return Stream.stream_cell(func)

    def _exec(self):
        if self.s:
            return RealTimeQueue(self.f, self.r, self.s.tail())
        f = RealTimeQueue._rotate(self.f, self.r, Stream())
        return RealTimeQueue(f, ListStack(), f)

    def snoc(self, value):
        return RealTimeQueue(self.f, self.r.cons(value), self.s)._exec()

    def head(self):
        if not self:
            raise IndexError("head from empty queue")
        return self.f.head()

    def tail(self):
        if not self:
            raise IndexError("tail from empty queue")
        return RealTimeQueue(self.f.tail(), self.r, self.s)._exec()
