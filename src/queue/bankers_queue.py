from __future__ import annotations
from typing import TypeVar, Generic, Optional
from src.basic.stream import Stream  # type: ignore


T = TypeVar('T')


class BankersQueue(Generic[T]):
    def __init__(self,
                 fsize: int = 0, f: Optional[Stream[T]] = None,
                 rsize: int = 0, r: Optional[Stream[T]] = None) -> None:
        self.fsize: int = fsize
        self.f: Stream[T] = Stream() if f is None else f
        self.rsize: int = rsize
        self.r: Stream[T] = Stream() if r is None else r

    def __bool__(self) -> bool:
        return self.fsize != 0

    def _normalize(self) -> BankersQueue[T]:
        if self.fsize >= self.rsize:
            return self
        else:
            lazy_rotate = self.f.concat(self.r.reverse())
            return BankersQueue(self.fsize + self.rsize, lazy_rotate,
                                0, Stream())

    def snoc(self, value: T) -> BankersQueue[T]:
        return BankersQueue[T](self.fsize, self.f,
                               self.rsize + 1, self.r.cons(value))._normalize()

    def head(self) -> T:
        if not self:
            raise IndexError("head from empty queue")
        head: T = self.f.head()
        return head

    def tail(self) -> BankersQueue[T]:
        if not self:
            raise IndexError("tail from empty queue")
        return BankersQueue[T](self.fsize - 1, self.f.tail(),
                               self.rsize, self.r)._normalize()
