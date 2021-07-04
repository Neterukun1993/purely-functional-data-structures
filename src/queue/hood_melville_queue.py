from src.basic.list_stack import ListStack


class RotationState:
    def __init__(self):
        raise NotImplementedError()

    def invalidate(self):
        raise NotImplementedError()

    def exec(self):
        raise NotImplementedError()


class Idle(RotationState):
    def __init__(self):
        pass

    def invalidate(self):
        return self

    def exec(self):
        return self


class Reversing(RotationState):
    def __init__(self, ok, f, fp, r, rp):
        self.ok = ok
        self.f = f
        self.fp = fp
        self.r = r
        self.rp = rp

    def invalidate(self):
        return Reversing(self.ok - 1, self.f, self.fp, self.r, self.rp)

    def exec(self):
        if not self.f and not self.r.tail():
            return Appending(self.ok, self.fp, self.rp.cons(self.r.head()))
        return Reversing(self.ok + 1, self.f.tail(),
                         self.fp.cons(self.f.head()), self.r.tail(),
                         self.rp.cons(self.r.head()))


class Appending(RotationState):
    def __init__(self, ok, f, r):
        self.ok = ok
        self.f = f
        self.r = r

    def invalidate(self):
        if self.ok == 0:
            return Done(self.r.tail())
        return Appending(self.ok - 1, self.f, self.r)

    def exec(self):
        if self.ok == 0:
            return Done(self.r)
        return Appending(self.ok - 1, self.f.tail(),
                         self.r.cons(self.f.head()))


class Done(RotationState):
    def __init__(self, f):
        self.f = f

    def invalidate(self):
        return self

    def exec(self):
        return self


class HoodMelvilleQueue:
    def __init__(self, fsize=0, f=None, state=None, rsize=0, r=None):
        self.fsize = fsize
        self.f = f if f is not None else ListStack()
        self.state = state if f is not None else Idle()
        self.rsize = rsize
        self.r = r if r is not None else ListStack()

    def __bool__(self):
        return self.fsize != 0

    def _exec(self):
        new_state = self.state.exec().exec()
        if type(new_state) is Done:
            return HoodMelvilleQueue(self.fsize, new_state.f, Idle(),
                                     self.rsize, self.r)
        return HoodMelvilleQueue(self.fsize, self.f, new_state,
                                 self.rsize, self.r)

    def _check(self):
        if self.rsize <= self.fsize:
            return self._exec()
        new_state = Reversing(0, self.f, ListStack(), self.r, ListStack())
        return HoodMelvilleQueue(self.fsize + self.rsize, self.f, new_state,
                                 0, ListStack())._exec()

    def snoc(self, value):
        return HoodMelvilleQueue(self.fsize, self.f, self.state,
                                 self.rsize + 1, self.r.cons(value))._check()

    def head(self):
        if not self:
            raise IndexError("head from empty queue")
        return self.f.head()

    def tail(self):
        if not self:
            raise IndexError("tail from empty queue")
        new_state = self.state.invalidate()
        return HoodMelvilleQueue(self.fsize - 1, self.f.tail(), new_state,
                                 self.rsize, self.r)._check()
