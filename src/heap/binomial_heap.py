from src.basic.list_stack import ListStack


class BinomialTree:
    def __init__(self, rank, value, children): 
        self.rank = rank
        self.value = value
        self.children = children

    @staticmethod
    def link(t1, t2):
        if t1.value < t2.value:
            return BinomialTree(t1.rank + 1, t1.value, t1.children.cons(t2))
        return BinomialTree(t1.rank + 1, t2.value, t2.children.cons(t1))


class BinomialHeap(ListStack):
    def _ins_tree(self, t):
        if not self:
            return self.cons(t)
        if t.rank < self.head().rank:
            return self.cons(t)
        else:
            return self.tail()._ins_tree(BinomialTree.link(t, self.head()))

    def _remove_min_tree(self):
        if not self.tail():
            return self.head(), BinomialHeap()
        t, tlist = self.tail()._remove_min_tree()
        if self.head().value <= t.value:
            return self.head(), self.tail()
        else:
            return t, tlist.cons(self.head())

    @staticmethod
    def merge(tl, tr):
        if not tl:
            return tr
        if not tr:
            return tl
        if tl.head().rank < tr.head().rank:
            return BinomialHeap.merge(tl.tail(), tr).cons(tl.head())
        elif tl.head().rank > tr.head().rank:
            return BinomialHeap.merge(tl, tr.tail()).cons(tr.head())
        else:
            return BinomialHeap.merge(tl.tail(), tr.tail())._ins_tree(
                   BinomialTree.link(tl.head(), tr.head()))

    def insert(self, value):
        return self._ins_tree(BinomialTree(0, value, BinomialHeap()))

    def find_min(self):
        t, _ = self._remove_min_tree()
        return t.value

    def delete_min(self):
        t, tlist = self._remove_min_tree()
        return BinomialHeap.merge(t.children.reverse(), tlist)
