from src.basic.list_stack import ListStack


class BatchedDeque:
    def __init__(self, fsize=0, f=None, rsize=0, r=None):
        self.fsize = fsize
        self.f = ListStack() if f is None else f
        self.rsize = rsize
        self.r = ListStack() if r is None else r

    def __bool__(self):
        return self.fsize + self.rsize != 0

    def _check(self):
        half = (self.fsize + self.rsize) // 2
        if self.fsize == 0:
            self.f = self.r.drop(half).reverse()
            self.r = self.r.take(half)
            self.fsize = self.rsize - half
            self.rsize = half
        elif self.rsize == 0:
            self.r = self.f.drop(half).reverse()
            self.f = self.f.take(half)
            self.rsize = self.fsize - half
            self.fsize = half
        return self

    def cons(self, value):
        return BatchedDeque(self.fsize + 1, self.f.cons(value),
                            self.rsize, self.r)._check()

    def head(self):
        if not self:
            raise IndexError("head from empty deque")
        if self.fsize == 0:
            return self.r.head()
        return self.f.head()

    def tail(self):
        if not self:
            raise IndexError("tail from empty deque")
        if self.fsize == 0:
            return BatchedDeque()
        return BatchedDeque(self.fsize - 1, self.f.tail(),
                            self.rsize, self.r)._check()

    def snoc(self, value):
        return BatchedDeque(self.fsize, self.f,
                            self.rsize + 1, self.r.cons(value))._check()

    def last(self):
        if not self:
            raise IndexError("last from empty deque")
        if self.rsize == 0:
            return self.f.head()
        return self.r.head()

    def init(self):
        if not self:
            raise IndexError("init from empty deque")
        if self.rsize == 0:
            return BatchedDeque()
        return BatchedDeque(self.fsize, self.f,
                            self.rsize - 1, self.r.tail())._check()
