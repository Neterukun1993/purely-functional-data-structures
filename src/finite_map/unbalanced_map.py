from __future__ import annotations
from typing import TypeVar, Generic, Optional
from src.basic.comparable import Comparable  # type: ignore
from src.basic.meta_singleton import MetaSingleton  # type: ignore


C = TypeVar('C', bound=Comparable)
T = TypeVar('T')


class UnbalancedMap(Generic[C, T], metaclass=MetaSingleton):
    key: C
    value: T
    tr: UnbalancedMap[C, T]
    tl: UnbalancedMap[C, T]

    def __init__(self, key: Optional[C] = None, value: Optional[T] = None,
                 tl: Optional[UnbalancedMap[C, T]] = None,
                 tr: Optional[UnbalancedMap[C, T]] = None) -> None:
        if key is not None:
            self.key = key
        if value is not None:
            self.value = value
        if tl is not None:
            self.tl = tl
        if tr is not None:
            self.tr = tr

    def __bool__(self) -> bool:
        return self is not UnbalancedMap()

    def lookup(self, key: C) -> T:
        if not self:
            raise KeyError
        elif key < self.key:
            return self.tl.lookup(key)
        elif key > self.key:
            return self.tr.lookup(key)
        return self.value

    def bind(self, key: C, value: T) -> UnbalancedMap[C, T]:
        if not self:
            return UnbalancedMap(key, value,
                                 UnbalancedMap(), UnbalancedMap())
        elif key < self.key:
            return UnbalancedMap(self.key, self.value,
                                 self.tl.bind(key, value), self.tr)
        elif key > self.key:
            return UnbalancedMap(self.key, self.value,
                                 self.tl, self.tr.bind(key, value))
        return UnbalancedMap(key, value, self.tl, self.tr)
