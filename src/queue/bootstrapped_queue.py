from __future__ import annotations
from typing import TypeVar, Generic, Optional
from src.basic.list_stack import ListStack  # type: ignore
from src.basic.suspension import Suspension  # type: ignore


T = TypeVar('T')


class BootstrappedQueue(Generic[T]):
    def __init__(
            self,
            fmsize: int = 0, f: Optional[ListStack[T]] = None,
            m: Optional[BootstrappedQueue[Suspension[ListStack[T]]]] = None,
            rsize: int = 0, r: Optional[ListStack[T]] = None) -> None:
        self.fmsize: int = fmsize
        self.f = ListStack() if f is None else f
        self.m = self if m is None else m
        self.rsize = rsize
        self.r = ListStack() if f is None else r

    def __bool__(self) -> bool:
        return self.fmsize + self.rsize != 0

    def _check_q(self) -> BootstrappedQueue[T]:
        if self.fmsize >= self.rsize:
            return self._check_f()
        else:
            susp = Suspension(lambda: self.r.reverse())
            return BootstrappedQueue[T](self.fmsize + self.rsize, self.f,
                                        self.m.snoc(susp), 0,
                                        ListStack())._check_f()

    def _check_f(self) -> BootstrappedQueue[T]:
        if not self.m and not self.f:
            return BootstrappedQueue[T]()
        if not self.f:
            return BootstrappedQueue[T](self.fmsize, self.m.head().force(),
                                        self.m.tail(), self.rsize, self.r)
        return self

    def snoc(self, value: T) -> BootstrappedQueue[T]:
        if not self:
            return BootstrappedQueue[T](1, ListStack().cons(value), self,
                                        0, ListStack())
        return BootstrappedQueue[T](self.fmsize, self.f, self.m,
                                    self.rsize + 1,
                                    self.r.cons(value))._check_q()

    def head(self) -> T:
        if not self:
            raise IndexError("head from empty queue")
        head: T = self.f.head()
        return head

    def tail(self) -> BootstrappedQueue[T]:
        if not self:
            raise IndexError("tail from empty queue")
        return BootstrappedQueue[T](self.fmsize - 1, self.f.tail(), self.m,
                                    self.rsize, self.r)._check_q()
