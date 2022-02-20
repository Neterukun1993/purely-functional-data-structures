from __future__ import annotations
from typing import TypeVar, Generic, Optional
from src.basic.stream import Stream  # type: ignore


T = TypeVar('T')


class RealTimeDeque(Generic[T]):
    CONSTANT: int = 2
    fsize: int
    f: Stream[T]
    sf: Stream[T]
    rsize: int
    r: Stream[T]
    sr: Stream[T]

    def __init__(self,
                 fsize: int = 0, f: Optional[Stream[T]] = None,
                 sf: Optional[Stream[T]] = None,
                 rsize: int = 0, r: Optional[Stream[T]] = None,
                 sr: Optional[Stream[T]] = None) -> None:
        self.fsize = fsize
        self.f = Stream() if f is None else f
        self.sf = Stream() if sf is None else sf
        self.rsize = rsize
        self.r = Stream() if r is None else r
        self.sr = Stream() if sr is None else sr

    def __bool__(self) -> bool:
        return self.fsize + self.rsize != 0

    def _exec1(self, s: Stream[T]) -> Stream[T]:
        return s.tail() if s else s

    def _exec2(self, s: Stream[T]) -> Stream[T]:
        return self._exec1(self._exec1(s))

    def _rotate_rev(self, f: Stream[T], r: Stream[T],
                    a: Stream[T]) -> Stream[T]:
        if not f:
            r.tail()
            return r.reverse().concat(a)
        func = lambda: (  # noqa: E731
            f.head(),
            self._rotate_rev(f.tail(), r.drop(self.CONSTANT),
                             r.take(self.CONSTANT).reverse().concat(a))
        )
        return Stream(func)

    def _rotate_drop(self, f: Stream[T], j: int, r: Stream[T]) -> Stream[T]:
        if j < self.CONSTANT:
            return self._rotate_rev(f, r.drop(j), Stream())
        func = lambda: (  # noqa: E731
            f.head(),
            self._rotate_drop(f.tail(), j - self.CONSTANT,
                              r.drop(self.CONSTANT))
        )
        return Stream(func)

    def _check(self) -> RealTimeDeque[T]:
        if self.fsize > self.CONSTANT * self.rsize + 1:
            i = (self.fsize + self.rsize) // 2
            j = self.fsize + self.rsize - i
            f = self.f.take(i)
            r = self._rotate_drop(self.r, i, self.f)
            return RealTimeDeque[T](i, f, f, j, r, r)
        elif self.rsize > self.CONSTANT * self.fsize + 1:
            j = (self.fsize + self.rsize) // 2
            i = self.fsize + self.rsize - j
            r = self.r.take(j)
            f = self._rotate_drop(self.f, j, self.r)
            return RealTimeDeque[T](i, f, f, j, r, r)
        return self

    def cons(self, value: T) -> RealTimeDeque[T]:
        sf = self._exec1(self.sf)
        sr = self._exec1(self.sr)
        return RealTimeDeque[T](self.fsize + 1, self.f.cons(value), sf,
                                self.rsize, self.r, sr)._check()

    def head(self) -> T:
        if not self:
            raise IndexError("head from empty deque")
        head: T = self.r.head() if self.fsize == 0 else self.f.head()
        return head

    def tail(self) -> RealTimeDeque[T]:
        if not self:
            raise IndexError("tail from empty deque")
        if self.fsize == 0:
            return RealTimeDeque()
        sf = self._exec2(self.sf)
        sr = self._exec2(self.sr)
        return RealTimeDeque[T](self.fsize - 1, self.f.tail(), sf,
                                self.rsize, self.r, sr)._check()

    def snoc(self, value: T) -> RealTimeDeque[T]:
        sf = self._exec1(self.sf)
        sr = self._exec1(self.sr)
        return RealTimeDeque[T](self.fsize, self.f, sf, self.rsize + 1,
                                self.r.cons(value), sr)._check()

    def last(self) -> T:
        if not self:
            raise IndexError("last from empty deque")
        last: T = self.f.head() if self.rsize == 0 else self.r.head()
        return last

    def init(self) -> RealTimeDeque[T]:
        if not self:
            raise IndexError("init from empty deque")
        if self.rsize == 0:
            return RealTimeDeque()
        sf = self._exec2(self.sf)
        sr = self._exec2(self.sr)
        return RealTimeDeque[T](self.fsize, self.f, sf,
                                self.rsize - 1, self.r.tail(), sr)._check()
