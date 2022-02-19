from __future__ import annotations
from typing import TypeVar, Generic, Optional
from src.basic.stream import Stream  # type: ignore


T = TypeVar('T')


class BankersDeque(Generic[T]):
    def __init__(self,
                 fsize: int = 0, f: Optional[Stream[T]] = None,
                 rsize: int = 0, r: Optional[Stream[T]] = None) -> None:
        self.fsize: int = fsize
        self.f: Stream[T] = Stream() if f is None else f
        self.rsize: int = rsize
        self.r: Stream[T] = Stream() if r is None else r

    def __bool__(self) -> bool:
        return self.fsize + self.rsize != 0

    def _check(self) -> BankersDeque[T]:
        if self.fsize > 2 * self.rsize + 1:
            i = (self.fsize + self.rsize) // 2
            j = self.fsize + self.rsize - i
            f = self.f.take(i)
            r = self.r.concat(self.f.drop(i).reverse())
            return BankersDeque[T](i, f, j, r)
        elif self.rsize > 2 * self.fsize + 1:
            j = (self.fsize + self.rsize) // 2
            i = self.fsize + self.rsize - j
            r = self.r.take(j)
            f = self.f.concat(self.r.drop(j).reverse())
            return BankersDeque[T](i, f, j, r)
        return self

    def cons(self, value: T) -> BankersDeque[T]:
        return BankersDeque[T](self.fsize + 1, self.f.cons(value),
                               self.rsize, self.r)._check()

    def head(self) -> T:
        if not self:
            raise IndexError("head from empty deque")
        head: T = self.r.head() if self.fsize == 0 else self.f.head()
        return head

    def tail(self) -> BankersDeque[T]:
        if not self:
            raise IndexError("tail from empty deque")
        if self.fsize == 0:
            return BankersDeque()
        return BankersDeque[T](self.fsize - 1, self.f.tail(),
                               self.rsize, self.r)._check()

    def snoc(self, value: T) -> BankersDeque[T]:
        return BankersDeque[T](self.fsize, self.f,
                               self.rsize + 1, self.r.cons(value))._check()

    def last(self) -> T:
        if not self:
            raise IndexError("last from empty deque")
        last: T = self.f.head() if self.rsize == 0 else self.r.head()
        return last

    def init(self) -> BankersDeque[T]:
        if not self:
            raise IndexError("init from empty deque")
        if self.rsize == 0:
            return BankersDeque()
        return BankersDeque[T](self.fsize, self.f,
                               self.rsize - 1, self.r.tail())._check()
