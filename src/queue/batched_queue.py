from __future__ import annotations
from typing import TypeVar, Generic, Optional
from src.basic.list_stack import ListStack  # type: ignore


T = TypeVar('T')


class BatchedQueue(Generic[T]):
    f: ListStack[T]
    r: ListStack[T]

    def __init__(self,
                 f: Optional[ListStack[T]] = None,
                 r: Optional[ListStack[T]] = None) -> None:
        self.f = ListStack() if f is None else f
        self.r = ListStack() if r is None else r

    def __bool__(self) -> bool:
        return self.f is not ListStack()

    def _check(self) -> BatchedQueue[T]:
        if not self.f:
            self.f = self.r.reverse()
            self.r = ListStack()
        return self

    def snoc(self, value: T) -> BatchedQueue[T]:
        return BatchedQueue[T](self.f, self.r.cons(value))._check()

    def head(self) -> T:
        if not self.f:
            raise IndexError("head from empty queue")
        head: T = self.f.head()
        return head

    def tail(self) -> BatchedQueue[T]:
        if not self.f:
            raise IndexError("tail from empty queue")
        return BatchedQueue[T](self.f.tail(), self.r)._check()
