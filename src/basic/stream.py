class Stream:
    Nil = None

    def __new__(cls, *args):
        if cls.Nil is None:
            cls.Nil = super().__new__(cls)
        return super().__new__(cls) if args else cls.Nil

    def __init__(self, strm=None):
        self.strm = strm

    def __bool__(self):
        return self is not Stream.Nil

    def __iter__(self):
        ptr = self
        while ptr:
            yield ptr.head()
            ptr = ptr.tail()

    def cons(self, value):
        return Stream((value, self))

    def head(self):
        if callable(self.strm):
            self.strm = self.strm()
        return self.strm[0]

    def tail(self):
        if callable(self.strm):
            self.strm = self.strm()
        return self.strm[1]

    @staticmethod
    def stream_cell(func):
        return Stream(func)

    def concat(self, other):
        if not self:
            return other
        func = lambda: (self.head(), self.tail().concat(other))
        return Stream(func)

    def reverse(self):
        def func():
            ret = Stream.Nil
            for x in self:
                ret = ret.cons(x)
            return ret.strm
        return Stream(func)

    def take(self, n):
        if n == 0 or not self:
            return Stream.Nil
        func = lambda: (self.head(), self.tail().take(n - 1))
        return Stream(func)

    def drop(self, n):
        def func():
            ret = self
            for _ in range(n):
                if not ret:
                    break
                ret = ret.tail()
            if ret:
                ret.tail()
            return ret.strm
        return Stream(func)
