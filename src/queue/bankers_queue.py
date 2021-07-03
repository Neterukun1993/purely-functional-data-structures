from src.basic.stream import Stream


class BankersQueue:
    def __init__(self, fsize=0, f=None, rsize=0, r=None):
        self.fsize = fsize
        self.f = Stream() if f is None else f
        self.rsize = rsize
        self.r = Stream() if r is None else r

    def __bool__(self):
        return self.fsize != 0

    def _normalize(self):
        if self.fsize >= self.rsize:
            return self
        else:
            lazy_rotate = self.f.concat(self.r.reverse())
            return BankersQueue(self.fsize + self.rsize, lazy_rotate,
                                0, Stream())

    def snoc(self, value):
        return BankersQueue(self.fsize, self.f,
                            self.rsize + 1, self.r.cons(value))._normalize()

    def head(self):
        if not self:
            raise IndexError("head from empty queue")
        return self.f.head()

    def tail(self):
        if not self:
            raise IndexError("tail from empty queue")
        return BankersQueue(self.fsize - 1, self.f.tail(),
                            self.rsize, self.r)._normalize()
