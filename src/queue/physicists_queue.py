from __future__ import annotations
from typing import TypeVar, Generic, Optional
from src.basic.list_stack import ListStack  # type: ignore
from src.basic.suspension import Suspension  # type: ignore


T = TypeVar('T')


class PhysicistsQueue(Generic[T]):
    working: ListStack[T]
    fsize: int
    f: Suspension[ListStack[T]]
    rsize: int
    r: ListStack[T]

    def __init__(self,
                 w: Optional[ListStack[T]] = None,
                 fsize: int = 0, f: Suspension[ListStack[T]] = None,
                 rsize: int = 0, r: ListStack[T] = None) -> None:
        self.working = ListStack() if w is None else w
        self.fsize = fsize
        self.f = (Suspension(lambda: ListStack()) if f is None else f)
        self.rsize = rsize
        self.r = ListStack() if r is None else r

    def __bool__(self) -> bool:
        return self.fsize != 0

    def _checkw(self) -> PhysicistsQueue[T]:
        if not self.working:
            return PhysicistsQueue[T](self.f.force(), self.fsize, self.f,
                                      self.rsize, self.r)
        else:
            return self

    def _check(self) -> PhysicistsQueue[T]:
        if self.rsize <= self.fsize:
            return self._checkw()
        f = self.f.force()
        susp = Suspension(lambda: f.concat(self.r.reverse()))
        return PhysicistsQueue[T](f, self.fsize + self.rsize, susp,
                                  0, ListStack())._checkw()

    def snoc(self, value: T) -> PhysicistsQueue[T]:
        return PhysicistsQueue[T](self.working, self.fsize, self.f,
                                  self.rsize + 1, self.r.cons(value))._check()

    def head(self) -> T:
        if not self.working:
            raise IndexError("head from empty queue")
        head: T = self.working.head()
        return head

    def tail(self) -> PhysicistsQueue[T]:
        if not self.working:
            raise IndexError("tail from empty queue")
        susp = Suspension(lambda: self.f.force().tail())
        return PhysicistsQueue[T](self.working.tail(), self.fsize - 1, susp,
                                  self.rsize, self.r)._check()
