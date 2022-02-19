from __future__ import annotations
from typing import TypeVar, Generic, Optional
from src.basic.list_stack import ListStack  # type: ignore


T = TypeVar('T')


class BatchedDeque(Generic[T]):
    def __init__(self,
                 fsize: int = 0, f: Optional[ListStack[T]] = None,
                 rsize: int = 0, r: Optional[ListStack[T]] = None) -> None:
        self.fsize: int = fsize
        self.f: ListStack[T] = ListStack() if f is None else f
        self.rsize: int = rsize
        self.r: ListStack[T] = ListStack() if r is None else r

    def __bool__(self) -> bool:
        return self.fsize + self.rsize != 0

    def _check(self) -> BatchedDeque[T]:
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

    def cons(self, value: T) -> BatchedDeque[T]:
        return BatchedDeque[T](self.fsize + 1, self.f.cons(value),
                               self.rsize, self.r)._check()

    def head(self) -> T:
        if not self:
            raise IndexError("head from empty deque")
        head: T = self.r.head() if self.fsize == 0 else self.f.head()
        return head

    def tail(self) -> BatchedDeque[T]:
        if not self:
            raise IndexError("tail from empty deque")
        if self.fsize == 0:
            return BatchedDeque[T]()
        return BatchedDeque[T](self.fsize - 1, self.f.tail(),
                               self.rsize, self.r)._check()

    def snoc(self, value: T) -> BatchedDeque[T]:
        return BatchedDeque[T](self.fsize, self.f,
                               self.rsize + 1, self.r.cons(value))._check()

    def last(self) -> T:
        if not self:
            raise IndexError("last from empty deque")
        last: T = self.f.head() if self.rsize == 0 else self.r.head()
        return last

    def init(self) -> BatchedDeque[T]:
        if not self:
            raise IndexError("init from empty deque")
        if self.rsize == 0:
            return BatchedDeque()
        return BatchedDeque[T](self.fsize, self.f,
                               self.rsize - 1, self.r.tail())._check()
