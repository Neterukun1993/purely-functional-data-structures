from __future__ import annotations
from typing import TypeVar, Generic, Optional, Iterator
from src.basic.meta_singleton import MetaSingleton  # type: ignore


T = TypeVar('T')


class ListStack(Generic[T], metaclass=MetaSingleton):
    _head: T
    _tail: ListStack[T]

    def __init__(self,
                 head: Optional[T] = None,
                 tail: Optional[ListStack[T]] = None) -> None:
        if head is not None:
            self._head = head
        if tail is not None:
            self._tail = tail

    def __bool__(self) -> bool:
        return self is not ListStack[T]()

    def __iter__(self) -> Iterator[T]:
        ptr = self
        while ptr:
            yield ptr.head()
            ptr = ptr.tail()

    def cons(self, value: T) -> ListStack[T]:
        return ListStack[T](value, self)

    def head(self) -> T:
        if self is ListStack[T]():
            raise IndexError("head from empty list")
        return self._head

    def tail(self) -> ListStack[T]:
        if self is ListStack[T]():
            raise IndexError("tail from empty list")
        return self._tail

    def reverse(self) -> ListStack[T]:
        ret = ListStack[T]()
        for x in self:
            ret = ret.cons(x)
        return ret

    def concat(self, other: ListStack[T]) -> ListStack[T]:
        ret = other
        for x in self.reverse():
            ret = ret.cons(x)
        return ret

    def take(self, n: int) -> ListStack[T]:
        ret = ListStack[T]()
        for i, x in enumerate(self):
            if i == n:
                break
            ret = ret.cons(x)
        return ret.reverse()

    def drop(self, n: int) -> ListStack[T]:
        ret = self
        for _ in range(n):
            if not ret:
                break
            ret = ret.tail()
        return ret
