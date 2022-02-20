from __future__ import annotations
from typing import TypeVar, Generic, Optional
from src.basic.comparable import Comparable  # type: ignore
from src.basic.meta_singleton import MetaSingleton  # type: ignore


T = TypeVar('T', bound=Comparable)
B, R = 0, 1


class RedBlackSet(Generic[T], metaclass=MetaSingleton):
    color: int
    value: T
    tl: RedBlackSet[T]
    tr: RedBlackSet[T]

    def __init__(self, color: int = B, value: Optional[T] = None,
                 tl: Optional[RedBlackSet[T]] = None,
                 tr: Optional[RedBlackSet[T]] = None) -> None:
        self.color = color
        if value is not None:
            self.value = value
        if tl is not None:
            self.tl = tl
        if tr is not None:
            self.tr = tr

    def __bool__(self) -> bool:
        return self is not RedBlackSet()

    def _balance(self) -> RedBlackSet[T]:
        if self.color == B and self.tl.color == R and self.tl.tl.color == R:
            value = self.tl.value
            tl = RedBlackSet(B, self.tl.tl.value, self.tl.tl.tl, self.tl.tl.tr)
            tr = RedBlackSet(B, self.value, self.tl.tr, self.tr)
            return RedBlackSet(R, value, tl, tr)
        if self.color == B and self.tl.color == R and self.tl.tr.color == R:
            value = self.tl.tr.value
            tl = RedBlackSet(B, self.tl.value, self.tl.tl, self.tl.tr.tl)
            tr = RedBlackSet(B, self.value, self.tl.tr.tr, self.tr)
            return RedBlackSet(R, value, tl, tr)
        if self.color == B and self.tr.color == R and self.tr.tl.color == R:
            value = self.tr.tl.value
            tl = RedBlackSet(B, self.value, self.tl, self.tr.tl.tl)
            tr = RedBlackSet(B, self.tr.value, self.tr.tl.tr, self.tr.tr)
            return RedBlackSet(R, value, tl, tr)
        if self.color == B and self.tr.color == R and self.tr.tr.color == R:
            value = self.tr.value
            tl = RedBlackSet(B, self.value, self.tl, self.tr.tl)
            tr = RedBlackSet(B, self.tr.tr.value, self.tr.tr.tl, self.tr.tr.tr)
            return RedBlackSet(R, value, tl, tr)
        return self

    def member(self, value: T) -> bool:
        if not self:
            return False
        elif value < self.value:
            return self.tl.member(value)
        elif value > self.value:
            return self.tr.member(value)
        return True

    def insert(self, value: T) -> RedBlackSet[T]:
        def ins(s: RedBlackSet[T]) -> RedBlackSet[T]:
            if not s:
                return RedBlackSet(R, value, RedBlackSet(), RedBlackSet())
            elif value < s.value:
                return RedBlackSet(s.color, s.value,
                                   ins(s.tl), s.tr)._balance()
            elif value > s.value:
                return RedBlackSet(s.color, s.value,
                                   s.tl, ins(s.tr))._balance()
            return s
        set_ = ins(self)
        set_.color = B
        return set_
