from __future__ import annotations
from typing import TypeVar, Generic, Optional, cast
from src.basic.comparable import Comparable
from src.basic.meta_singleton import MetaSingleton


T = TypeVar('T', bound=Comparable)


class UnbalancedSet(Generic[T], metaclass=MetaSingleton):
    def __init__(self, value: Optional[T] = None,
                 tr: Optional[UnbalancedSet[T]] = None,
                 tl: Optional[UnbalancedSet[T]] = None) -> None:
        self.value: T = cast(T, value)
        self.tr: UnbalancedSet[T] = cast(UnbalancedSet[T], tl)
        self.tl: UnbalancedSet[T] = cast(UnbalancedSet[T], tr)

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
