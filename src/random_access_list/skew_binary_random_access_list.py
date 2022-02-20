from __future__ import annotations
from typing import TypeVar, Generic, Union, Optional
from src.basic.list_stack import ListStack  # type: ignore


T = TypeVar('T')


class Leaf(Generic[T]):
    value: T

    def __init__(self, value: T) -> None:
        self.value = value

    def lookup_tree(self, i: int, size: int) -> T:
        if i == 0:
            return self.value
        raise IndexError

    def update_tree(self, i: int, size: int, value: T) -> Leaf[T]:
        if i == 0:
            return Leaf(value)
        raise IndexError


class Node(Generic[T]):
    value: T
    tl: Tree[T]
    tr: Tree[T]

    def __init__(self, value: T, tl: Tree[T], tr: Tree[T]) -> None:
        self.value = value
        self.tl = tl
        self.tr = tr

    def lookup_tree(self, i: int, size: int) -> T:
        if i == 0:
            return self.value
        elif i <= size // 2:
            return self.tl.lookup_tree(i - 1, size // 2)
        else:
            return self.tr.lookup_tree(i - 1 - size // 2, size // 2)

    def update_tree(self, i: int, size: int, value: T) -> Node[T]:
        if i == 0:
            return Node(value, self.tl, self.tr)
        elif i <= size // 2:
            return Node(self.value,
                        self.tl.update_tree(i - 1, size // 2, value),
                        self.tr)
        else:
            return Node(self.value,
                        self.tl,
                        self.tr.update_tree(i - 1 - size // 2, size // 2,
                                            value))


Tree = Union[Node[T], Leaf[T]]


class SkewBinaryRandomAccessList(Generic[T]):
    rlist: ListStack[Tree[T]]

    def __init__(self, rlist: Optional[ListStack[Tree[T]]] = None) -> None:
        self.rlist = ListStack() if rlist is None else rlist

    def __bool__(self) -> bool:
        return self.rlist is not ListStack()

    def cons(self, value: T) -> SkewBinaryRandomAccessList[T]:
        if self.rlist and self.rlist.tail():
            sz1, tr1 = self.rlist.head()
            sz2, tr2 = self.rlist.tail().head()
            if sz1 == sz2:
                size = 1 + sz1 + sz2
                tree = Node(value, tr1, tr2)
                list_ = self.rlist.tail().tail()
                return SkewBinaryRandomAccessList(list_.cons((size, tree)))
        return SkewBinaryRandomAccessList(self.rlist.cons((1, Leaf(value))))

    def head(self) -> T:
        if not self.rlist:
            raise IndexError("head from empty list")
        size, tree = self.rlist.head()
        value: T = tree.value
        return value

    def tail(self) -> SkewBinaryRandomAccessList[T]:
        if not self.rlist:
            raise IndexError("tail from empty list")
        size, tree = self.rlist.head()
        list_ = self.rlist.tail()
        if size != 1:
            list_ = list_.cons((size // 2, tree.tr)).cons((size // 2, tree.tl))
        return SkewBinaryRandomAccessList(list_)

    def lookup(self, i: int) -> T:
        list_ = self.rlist
        while list_:
            size, tree = list_.head()
            if i < size:
                value: T = tree.lookup_tree(i, size)
                return value
            i -= size
            list_ = list_.tail()
        raise IndexError("list index out of range")

    def update(self, i: int, value: T) -> SkewBinaryRandomAccessList[T]:

        def inner_update(list_: ListStack[Tree[T]], i: int,
                         value: T) -> ListStack[Tree[T]]:
            if not list_:
                raise IndexError("list assignment index out of range")
            size, tree = list_.head()
            list_ = list_.tail()
            if i < size:
                return list_.cons((size, tree.update_tree(i, size, value)))
            else:
                return inner_update(list_, i - size, value).cons((size, tree))

        return SkewBinaryRandomAccessList(inner_update(self.rlist, i, value))
