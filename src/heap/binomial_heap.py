from __future__ import annotations
from typing import TypeVar, Generic, Tuple, cast
from src.basic.meta_singleton import MetaSingleton
from src.basic.list_stack import ListStack
from src.basic.comparable import Comparable


T = TypeVar('T', bound=Comparable)


class BinomialTree(Generic[T]):
    def __init__(self,
                 rank: int,
                 value: T,
                 children: ListStack[BinomialTree[T]]) -> None:
        self.rank = rank
        self.value = value
        self.children = children

    @staticmethod
    def link(t1: BinomialTree[T], t2: BinomialTree[T]) -> BinomialTree[T]:
        if t1.value < t2.value:
            return BinomialTree(t1.rank + 1, t1.value, t1.children.cons(t2))
        return BinomialTree(t1.rank + 1, t2.value, t2.children.cons(t1))


class BinomialHeap(Generic[T]):
    def __init__(self, heap: ListStack[BinomialTree[T]]
                 = ListStack[BinomialTree[T]]()) -> None:
        self.heap = heap

    def __bool__(self) -> bool:
        return self.heap is not ListStack[BinomialTree[T]]()

    def _cons(self, tree: BinomialTree[T]) -> BinomialHeap[T]:
        return BinomialHeap(self.heap.cons(tree))

    def _head(self) -> BinomialTree[T]:
        return cast(BinomialTree[T], self.heap.head())

    def _tail(self) -> BinomialHeap[T]:
        return BinomialHeap(self.heap.tail())

    def _ins_tree(self, tree: BinomialTree[T]) -> BinomialHeap[T]:
        if not self:
            return self._cons(tree)
        if tree.rank < self._head().rank:
            return self._cons(tree)
        else:
            return self._tail()\
                   ._ins_tree(BinomialTree.link(tree, self._head()))

    def _remove_min_tree(self) -> Tuple[BinomialTree[T], BinomialHeap[T]]:
        if not self._tail():
            return self._head(), BinomialHeap[T]()
        tree, heap = self._tail()._remove_min_tree()
        if self._head().value <= tree.value:
            return self._head(), self._tail()
        else:
            return tree, heap._cons(self._head())

    @staticmethod
    def merge(hl: BinomialHeap[T], hr: BinomialHeap[T]) -> BinomialHeap[T]:
        if not hl:
            return hr
        if not hr:
            return hl
        if hl._head().rank < hr._head().rank:
            return BinomialHeap.merge(hl._tail(), hr)._cons(hl._head())
        elif hl._head().rank > hr._head().rank:
            return BinomialHeap.merge(hl, hr._tail())._cons(hr._head())
        else:
            return BinomialHeap.merge(hl._tail(), hr._tail())\
                   ._ins_tree(BinomialTree.link(hl._head(), hr._head()))

    def insert(self, value: T) -> BinomialHeap[T]:
        return self._ins_tree(BinomialTree(0, value,
                                           ListStack[BinomialTree[T]]()))

    def find_min(self) -> T:
        tree, _ = self._remove_min_tree()
        return tree.value

    def delete_min(self) -> BinomialHeap[T]:
        tree, heap = self._remove_min_tree()
        return BinomialHeap.merge(BinomialHeap(tree.children.reverse()), heap)
