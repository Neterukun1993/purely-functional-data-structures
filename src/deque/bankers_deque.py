from src.basic.stream import Stream


class BankersDeque:
    def __init__(self, fsize=0, f=None, rsize=0, r=None):
        self.fsize = fsize
        self.f = Stream() if f is None else f
        self.rsize = rsize
        self.r = Stream() if r is None else r

    def __bool__(self):
        return self.fsize + self.rsize != 0

    def _check(self):
        if self.fsize > 2 * self.rsize + 1:
            i = (self.fsize + self.rsize) // 2
            j = self.fsize + self.rsize - i
            f = self.f.take(i)
            r = self.r.concat(self.f.drop(i).reverse())
            return BankersDeque(i, f, j, r)
        elif self.rsize > 2 * self.fsize + 1:
            j = (self.fsize + self.rsize) // 2
            i = self.fsize + self.rsize - j
            r = self.r.take(j)
            f = self.f.concat(self.r.drop(j).reverse())
            return BankersDeque(i, f, j, r)
        return self

    def cons(self, value):
        return BankersDeque(self.fsize + 1, self.f.cons(value),
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
            return BankersDeque()
        return BankersDeque(self.fsize - 1, self.f.tail(),
                            self.rsize, self.r)._check()

    def snoc(self, value):
        return BankersDeque(self.fsize, self.f,
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
            return BankersDeque()
        return BankersDeque(self.fsize, self.f,
                            self.rsize - 1, self.r.tail())._check()
