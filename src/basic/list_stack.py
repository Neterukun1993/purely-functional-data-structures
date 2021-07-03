from src.basic.meta_singleton import MetaSingleton


class ListStack(metaclass=MetaSingleton):
    def __init__(self, head=None, tail=None):
        self._head = head
        self._tail = tail

    def __bool__(self):
        return self is not ListStack.Nil[ListStack]

    def __iter__(self):
        ptr = self
        while ptr:
            yield ptr.head()
            ptr = ptr.tail()

    def cons(self, value):
        return ListStack(value, self)

    def head(self):
        if self is ListStack.Nil[ListStack]:
            raise IndexError("pop from empty list")
        return self._head

    def tail(self):
        if self is ListStack.Nil[ListStack]:
            raise IndexError("pop from empty list")
        return self._tail

    def reverse(self):
        ret = ListStack.Nil[ListStack]
        for x in self:
            ret = ret.cons(x)
        return ret

    def concat(self, other):
        ret = other
        for x in self.reverse():
            ret = ret.cons(x)
        return ret
