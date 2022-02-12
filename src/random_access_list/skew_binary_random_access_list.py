from src.basic.list_stack import ListStack


class Leaf:
    def __init__(self, value):
        self.value = value

    def lookup_tree(self, i, size):
        if i == 0:
            return self.value
        raise IndexError

    def update_tree(self, i, size, value):
        if i == 0:
            return Leaf(value)
        raise IndexError


class Node:
    def __init__(self, value, tl, tr):
        self.value = value
        self.tl = tl
        self.tr = tr

    def lookup_tree(self, i, size):
        if i == 0:
            return self.value
        elif i <= size // 2:
            return self.tl.lookup_tree(i - 1, size // 2)
        else:
            return self.tr.lookup_tree(i - 1 - size // 2, size // 2)

    def update_tree(self, i, size, value):
        if i == 0:
            return Node(value, self.tl, self.tr)
        elif i <= size // 2:
            return Node(self.value,
                        self.tl.update_tree(i - 1, size // 2, value),
                        self.tr)
        else:
            return Node(self.value,
                        self.tl,
                        self.tr.update_tree(i - 1 - size // 2, size // 2, value))


class SkewBinaryRandomAccessList:
    def __init__(self, list_=None):
        self.rlist = list_ if list_ is not None else ListStack()

    def __bool__(self):
        return self.rlist is not ListStack()

    def cons(self, value):
        if self.rlist and self.rlist.tail():
            sz1, tr1 = self.rlist.head()
            sz2, tr2 = self.rlist.tail().head()
            if sz1 == sz2:
                size = 1 + sz1 + sz2
                tree = Node(value, tr1, tr2)
                list_ = self.rlist.tail().tail()
                return SkewBinaryRandomAccessList(list_.cons((size, tree)))
        return SkewBinaryRandomAccessList(self.rlist.cons((1, Leaf(value))))

    def head(self):
        if not self.rlist:
            raise IndexError("head from empty list")
        size, tree = self.rlist.head()
        return tree.value

    def tail(self):
        if not self.rlist:
            raise IndexError("tail from empty list")
        size, tree = self.rlist.head()
        list_ = self.rlist.tail()
        if size != 1:
            list_ = list_.cons((size // 2, tree.tr)).cons((size // 2, tree.tl))
        return SkewBinaryRandomAccessList(list_)

    def lookup(self, i):
        list_ = self.rlist
        while list_:
            size, tree = list_.head()
            if i < size:
                return tree.lookup_tree(i, size)
            i -= size
            list_ = list_.tail()
        raise IndexError("list index out of range")

    def update(self, i, value):

        def inner_update(list_, i, value):
            if not list_:
                raise IndexError("list assignment index out of range")
            size, tree = list_.head()
            list_ = list_.tail()
            if i < size:
                return list_.cons((size, tree.update_tree(i, size, value)))
            else:
                return inner_update(list_, i - size, value).cons((size, tree))

        return SkewBinaryRandomAccessList(inner_update(self.rlist, i, value))
