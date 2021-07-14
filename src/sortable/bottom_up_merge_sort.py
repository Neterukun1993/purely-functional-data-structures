from __future__ import annotations
from typing import TypeVar, Generic
from src.basic.list_stack import ListStack
from src.basic.suspension import Suspension


T = TypeVar('T')


class BottomUpMergeSort(Generic[T]):
    def __init__(self, size: int = 0,
                 segs: Suspension[ListStack[ListStack[T]]]
                 = Suspension(ListStack())) -> None:
        self.size: int = size
        self.segs: Suspension[ListStack[ListStack[T]]] = segs

    def __bool__(self) -> bool:
        return self.size != 0

    @staticmethod
    def _merge(xs: ListStack[T], ys: ListStack[T]) -> ListStack[T]:
        if not xs:
            return ys
        if not ys:
            return xs
        if xs.head() <= ys.head():
            return BottomUpMergeSort._merge(xs.tail(), ys).cons(xs.head())
        return BottomUpMergeSort._merge(xs, ys.tail()).cons(ys.head())

    def add(self, value: T) -> BottomUpMergeSort[T]:
        def add_seg(seg: ListStack[T], seg_list: ListStack[ListStack[T]],
                    size: int) -> ListStack[T]:
            if size % 2 == 0:
                return seg_list.cons(seg)
            return add_seg(BottomUpMergeSort._merge(seg, seg_list.head()),
                           seg_list.tail(), size // 2)

        func = (lambda: add_seg(ListStack().cons(value),
                                self.segs.force(), self.size))
        susp = Suspension(func)
        return BottomUpMergeSort(self.size + 1, susp)

    def sort(self) -> ListStack[T]:
        def merge_all(xs: ListStack[T],
                      seg_list: ListStack[ListStack[T]]) -> ListStack[T]:
            if not seg_list:
                return xs
            return merge_all(BottomUpMergeSort._merge(xs, seg_list.head()),
                             seg_list.tail())

        return merge_all(ListStack(), self.segs.force())
