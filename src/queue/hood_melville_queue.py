from __future__ import annotations
from typing import TypeVar, Generic, Optional, Union, cast
from src.basic.list_stack import ListStack  # type: ignore


T = TypeVar('T')


class RotationState:
    def __init__(self) -> None:
        raise NotImplementedError()

    def invalidate(self) -> RotationState:
        raise NotImplementedError()

    def exec(self) -> RotationState:
        raise NotImplementedError()


class Idle(RotationState):
    def __init__(self) -> None:
        pass

    def invalidate(self) -> Idle:
        return self

    def exec(self) -> Idle:
        return self


class Reversing(Generic[T], RotationState):
    def __init__(self, ok: int, f: ListStack[T], fp: ListStack[T],
                 r: ListStack[T], rp: ListStack[T]) -> None:
        self.ok: int = ok
        self.f: ListStack[T] = f
        self.fp: ListStack[T] = fp
        self.r: ListStack[T] = r
        self.rp: ListStack[T] = rp

    def invalidate(self) -> Reversing[T]:
        return Reversing[T](self.ok - 1, self.f, self.fp, self.r, self.rp)

    def exec(self) -> Union[Appending[T], Reversing[T]]:
        if not self.f and not self.r.tail():
            return Appending[T](self.ok, self.fp, self.rp.cons(self.r.head()))
        return Reversing[T](self.ok + 1, self.f.tail(),
                            self.fp.cons(self.f.head()), self.r.tail(),
                            self.rp.cons(self.r.head()))


class Appending(Generic[T], RotationState):
    def __init__(self, ok: int, f: ListStack[T], r: ListStack[T]) -> None:
        self.ok: int = ok
        self.f: ListStack[T] = f
        self.r: ListStack[T] = r

    def invalidate(self) -> Union[Appending[T], Done[T]]:
        if self.ok == 0:
            return Done[T](self.r.tail())
        return Appending[T](self.ok - 1, self.f, self.r)

    def exec(self) -> Union[Appending[T], Done[T]]:
        if self.ok == 0:
            return Done[T](self.r)
        return Appending[T](self.ok - 1, self.f.tail(),
                            self.r.cons(self.f.head()))


class Done(Generic[T], RotationState):
    def __init__(self, f: ListStack[T]) -> None:
        self.f: ListStack[T] = f

    def invalidate(self) -> Done[T]:
        return self

    def exec(self) -> Done[T]:
        return self


class HoodMelvilleQueue(Generic[T]):
    def __init__(self,
                 fsize: int = 0, f: Optional[ListStack[T]] = None,
                 state: Optional[RotationState] = None,
                 rsize: int = 0, r: Optional[ListStack[T]] = None) -> None:
        self.fsize: int = fsize
        self.f: ListStack[T] = ListStack() if f is None else f
        self.state: RotationState = Idle() if state is None else state
        self.rsize: int = rsize
        self.r: ListStack[T] = ListStack() if r is None else r

    def __bool__(self) -> bool:
        return self.fsize != 0

    def _exec(self) -> HoodMelvilleQueue[T]:
        new_state = self.state.exec().exec()
        if type(new_state) is Done:
            new_state = cast(Done[T], new_state)
            return HoodMelvilleQueue[T](self.fsize, new_state.f, Idle(),
                                        self.rsize, self.r)
        return HoodMelvilleQueue[T](self.fsize, self.f, new_state,
                                    self.rsize, self.r)

    def _check(self) -> HoodMelvilleQueue[T]:
        if self.rsize <= self.fsize:
            return self._exec()
        new_state = Reversing[T](0, self.f, ListStack(), self.r, ListStack())
        return HoodMelvilleQueue[T](self.fsize + self.rsize, self.f, new_state,
                                    0, ListStack())._exec()

    def snoc(self, value: T) -> HoodMelvilleQueue[T]:
        return HoodMelvilleQueue[T](self.fsize, self.f, self.state,
                                    self.rsize + 1,
                                    self.r.cons(value))._check()

    def head(self) -> T:
        if not self:
            raise IndexError("head from empty queue")
        head: T = self.f.head()
        return head

    def tail(self) -> HoodMelvilleQueue[T]:
        if not self:
            raise IndexError("tail from empty queue")
        new_state = self.state.invalidate()
        return HoodMelvilleQueue[T](self.fsize - 1, self.f.tail(), new_state,
                                    self.rsize, self.r)._check()
