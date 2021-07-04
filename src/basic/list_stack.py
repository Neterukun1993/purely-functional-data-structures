from src.basic.meta_singleton import MetaSingleton


class ListStack(metaclass=MetaSingleton):
    def __init__(self, head=None, tail=None):
        self._head = head
        self._tail = tail

    def __bool__(self):
        return self is not self.__class__.Nil[self.__class__]

    def __iter__(self):
        ptr = self
        while ptr:
            yield ptr.head()
            ptr = ptr.tail()

    def cons(self, value):
        return self.__class__(value, self)

    def head(self):
        if self is self.__class__.Nil[self.__class__]:
            raise IndexError("pop from empty list")
        return self._head

    def tail(self):
        if self is self.__class__.Nil[self.__class__]:
            raise IndexError("pop from empty list")
        return self._tail

    def reverse(self):
        ret = self.__class__.Nil[self.__class__]
        for x in self:
            ret = ret.cons(x)
        return ret

    def concat(self, other):
        ret = other
        for x in self.reverse():
            ret = ret.cons(x)
        return ret

    def take(self, n):
        ret = self.__class__.Nil[self.__class__] 
        for i, x in enumerate(self):
            if i == n:
                break
            ret = ret.cons(x)
        return ret.reverse()

    def drop(self, n):
        ret = self
        for _ in range(n):
            if not ret:
                break
            ret = ret.tail()
        return ret
