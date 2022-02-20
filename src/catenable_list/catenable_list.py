from __future__ import annotations
from typing import TypeVar, Generic, Optional
from src.basic.meta_singleton import MetaSingleton  # type: ignore
from src.basic.suspension import Suspension  # type: ignore
from src.queue.real_time_queue import RealTimeQueue  # type: ignore


T = TypeVar('T')


class CatenableList(Generic[T], metaclass=MetaSingleton):
    _head: T
    q:  RealTimeQueue[Suspension[CatenableList[T]]]

    def __init__(self, _head: Optional[T] = None,
                 q: Optional[RealTimeQueue[T]] = None) -> None:
        if _head is not None:
            self._head = _head
        self.q = RealTimeQueue() if q is None else q

    def __bool__(self) -> bool:
        return self is not CatenableList()

    def _link(self, susp: Suspension[CatenableList[T]]) -> CatenableList[T]:
        return CatenableList[T](self._head, self.q.snoc(susp))

    @staticmethod
    def _link_all(
            q: RealTimeQueue[Suspension[CatenableList[T]]]
            ) -> CatenableList[T]:
        t: CatenableList[T] = q.head().force()
        q_tail = q.tail()
        if q_tail:
            susp = Suspension(lambda: CatenableList._link_all(q_tail))
            return t._link(susp)
        else:
            return t

    def concat(self, other: CatenableList[T]) -> CatenableList[T]:
        if not other:
            return self
        if not self:
            return other
        return self._link(Suspension(other))

    def cons(self, value: T) -> CatenableList[T]:
        return CatenableList(value, RealTimeQueue()).concat(self)

    def snoc(self, value: T) -> CatenableList[T]:
        return self.concat(CatenableList(value, RealTimeQueue()))

    def head(self) -> T:
        if not self:
            raise IndexError("head from empty list")
        return self._head

    def tail(self) -> CatenableList[T]:
        if not self:
            raise IndexError("tail from empty list")
        if self.q:
            return CatenableList._link_all(self.q)
        return CatenableList()
