from src.basic.suspension import Suspension


class Zero:
    def __init__(self):
        pass


class One:
    def __init__(self, x):
        self.x = x


class Two:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Shallow:
    def __init__(self, f):
        self.f = f


class Deep:
    def __init__(self, f, m, r):
        self.f = f
        self.m = m
        self.r = r


class ImplicitQueue:
    def __init__(self, que=None):
        self.que = Shallow(Zero()) if que is None else que

    def __bool__(self):
        if isinstance(self.que, Shallow) and isinstance(self.que.f, Zero):
            return False
        return True

    def snoc(self, value):
        if isinstance(self.que, Shallow):
            if isinstance(self.que.f, Zero):
                return ImplicitQueue(Shallow(One(value)))
            if isinstance(self.que.f, One):
                x = self.que.f.x
                susp = Suspension(lambda: ImplicitQueue())
                return ImplicitQueue(Deep(Two(x, value), susp, Zero()))

        if isinstance(self.que, Deep):
            if isinstance(self.que.r, Zero):
                return ImplicitQueue(Deep(self.que.f, self.que.m, One(value)))
            if isinstance(self.que.r, One):
                x = self.que.r.x
                susp = Suspension(lambda: self.que.m.force().snoc((x, value)))
                return ImplicitQueue(Deep(self.que.f, susp, Zero()))

    def head(self):
        if isinstance(self.que, Shallow):
            if isinstance(self.que.f, Zero):
                raise IndexError("head from empty queue")
            if isinstance(self.que.f, One):
                return self.que.f.x

        if isinstance(self.que, Deep):
            if isinstance(self.que.f, One):
                return self.que.f.x
            if isinstance(self.que.f, Two):
                return self.que.f.x

    def tail(self):
        if isinstance(self.que, Shallow):
            if isinstance(self.que.f, Zero):
                raise IndexError("tail from empty queue")
            if isinstance(self.que.f, One):
                return ImplicitQueue()

        if isinstance(self.que, Deep):
            if isinstance(self.que.f, Two):
                y = self.que.f.y
                return ImplicitQueue(Deep(One(y), self.que.m, self.que.r))
            if isinstance(self.que.f, One):
                if not self.que.m.force():
                    return ImplicitQueue(Shallow(self.que.r))
                else:
                    y, z = self.que.m.force().head()
                    susp = Suspension(lambda: self.que.m.force().tail())
                    return ImplicitQueue(Deep(Two(y, z), susp, self.que.r))
