from __future__ import annotations
from typing import TypeVar, Generic, Optional
from src.basic.comparable import Comparable  # type: ignore
from src.basic.meta_singleton import MetaSingleton  # type: ignore


T = TypeVar('T', bound=Comparable)


class UnbalancedSet(Generic[T], metaclass=MetaSingleton):
    value: T
    tr: UnbalancedSet[T]
    tl: UnbalancedSet[T]

    def __init__(self, value: Optional[T] = None,
                 tl: Optional[UnbalancedSet[T]] = None,
                 tr: Optional[UnbalancedSet[T]] = None) -> None:
        if value is not None:
            self.value = value
        if tl is not None:
            self.tl = tl
        if tr is not None:
            self.tr = tr

    def __bool__(self) -> bool:
        return self is not UnbalancedSet()

    def member(self, value: T) -> bool:
        if not self:
            return False
        elif value < self.value:
            return self.tl.member(value)
        elif value > self.value:
            return self.tr.member(value)
        return True

    def insert(self, value: T) -> UnbalancedSet[T]:
        if not self:
            return UnbalancedSet(value, UnbalancedSet(), UnbalancedSet())
        elif value < self.value:
            return UnbalancedSet(self.value, self.tl.insert(value), self.tr)
        elif value > self.value:
            return UnbalancedSet(self.value, self.tl, self.tr.insert(value))
        return self
