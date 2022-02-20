from __future__ import annotations
from typing import TypeVar, Generic, Optional
from src.basic.list_stack import ListStack  # type: ignore
from src.basic.stream import Stream  # type: ignore


T = TypeVar('T')


class RealTimeQueue(Generic[T]):
    f: Stream[T]
    r: ListStack[T]
    s: Stream[T]

    def __init__(self,
                 f: Optional[Stream[T]] = None,
                 r: Optional[ListStack[T]] = None,
                 s: Optional[Stream[T]] = None) -> None:
        self.f = Stream() if f is None else f
        self.r = ListStack() if r is None else r
        self.s = Stream() if s is None else s

    def __bool__(self) -> bool:
        return self.f is not Stream()

    @staticmethod
    def _rotate(f: Stream[T], r: ListStack[T], s: Stream[T]) -> Stream[T]:
        if not f:
            return s.cons(r.head())
        func = lambda: (  # noqa: E731
            f.head(),
            RealTimeQueue._rotate(f.tail(), r.tail(), s.cons(r.head()))
        )
        return Stream(func)

    def _exec(self) -> RealTimeQueue[T]:
        if self.s:
            return RealTimeQueue[T](self.f, self.r, self.s.tail())
        f = RealTimeQueue._rotate(self.f, self.r, Stream())
        return RealTimeQueue[T](f, ListStack(), f)

    def snoc(self, value: T) -> RealTimeQueue[T]:
        return RealTimeQueue[T](self.f, self.r.cons(value), self.s)._exec()

    def head(self) -> T:
        if not self:
            raise IndexError("head from empty queue")
        head: T = self.f.head()
        return head

    def tail(self) -> RealTimeQueue[T]:
        if not self:
            raise IndexError("tail from empty queue")
        return RealTimeQueue[T](self.f.tail(), self.r, self.s)._exec()
