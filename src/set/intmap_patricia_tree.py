class Leaf:
    def __init__(self, k, elem):
        self.k = k
        self.elem = elem


class Branch:
    def __init__(self, prefix, mask, l, r):
        self.prefix = prefix
        self.mask = mask
        self.l = l
        self.r = r

    @staticmethod
    def new(prefix, mask, l, r):
        if l is None: return r
        if r is None: return l
        return Branch(prefix, mask, l, r)

    def match_prefix(self, k):
        return k & (self.mask - 1) == self.prefix

    def zerobit(self, k):
        return k & self.mask == 0


class IntMapPatriciaTree:
    def __init__(self, root=None):
        self.root = root

    def __bool__(self):
        return self.root is not None

    def _branching_bit(self, p0, p1):
        x = p0 ^ p1
        return x & -x

    def _join(self, p0, t0, p1, t1):
        m = self._branching_bit(p0, p1)
        if p0 & m == 0: return Branch.new(p0 & (m - 1), m, t0, t1)
        else: return Branch.new(p0 & (m - 1), m, t1, t0)

    def lookup(self, k):
        def lkup(node):
            if node is None:
                return None
            if type(node) is Leaf:
                if k == node.k: return node.elem
                else: return None
            if type(node) is Branch:
                if not node.match_prefix(k): return None
                if node.zerobit(k): return lkup(node.l)
                return lkup(node.r)

        return lkup(self.root)

    def insert(self, k, elem):
        def ins(node):
            if node is None:
                return Leaf(k, elem)
            if type(node) is Leaf:
                if k == node.k: return Leaf(k, elem)
                else: return self._join(k, Leaf(k, elem), node.k, node)
            if type(node) is Branch:
                if not node.match_prefix(k):
                    return self._join(k, Leaf(k, elem), node.prefix, node)
                if node.zerobit(k):
                    return Branch.new(node.prefix, node.mask, ins(node.l), node.r)
                return Branch.new(node.prefix, node.mask, node.l, ins(node.r))

        return IntMapPatriciaTree(ins(self.root))
