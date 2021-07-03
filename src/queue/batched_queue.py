from src.basic.list_stack import ListStack


class BatchedQueue:
    def __init__(self, f=None, r=None):
        self.f = ListStack() if f is None else f
        self.r = ListStack() if r is None else r

    def __bool__(self):
        return self.f is not ListStack()

    def _check(self):
        if not self.f:
            self.f = self.r.reverse()
            self.r = ListStack()
        return self

    def snoc(self, value):
        return BatchedQueue(self.f, self.r.cons(value))._check()

    def head(self):
        if not self.f:
            raise IndexError("head from empty queue")
        return self.f.head()

    def tail(self):
        if not self.f:
            raise IndexError("tail from empty queue")
        return BatchedQueue(self.f.tail(), self.r)._check()
