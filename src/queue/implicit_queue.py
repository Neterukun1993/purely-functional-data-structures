from __future__ import annotations
from typing import TypeVar, Generic, Optional, Union
from src.basic.suspension import Suspension  # type: ignore


T = TypeVar('T')


class Zero:
    def __init__(self) -> None:
        pass


class One(Generic[T]):
    x: T

    def __init__(self, x: T) -> None:
        self.x = x


class Two(Generic[T]):
    x: T
    y: T

    def __init__(self, x: T, y: T) -> None:
        self.x = x
        self.y = y


Digit = Union[Zero, One[T], Two[T]]


class Shallow(Generic[T]):
    f: Digit[T]

    def __init__(self, f: Digit[T]) -> None:
        self.f = f


class Deep(Generic[T]):
    f: Digit[T]
    m: Suspension[ImplicitQueue[T]]
    r: Digit[T]

    def __init__(self, f: Digit[T],
                 m: Suspension[ImplicitQueue[T]], r: Digit[T]) -> None:
        self.f = f
        self.m = m
        self.r = r


class ImplicitQueue(Generic[T]):
    que: Union[Shallow[T], Deep[T]]

    def __init__(self,
                 que: Optional[Union[Shallow[T], Deep[T]]] = None) -> None:
        self.que = Shallow(Zero()) if que is None else que

    def __bool__(self) -> bool:
        if isinstance(self.que, Shallow) and isinstance(self.que.f, Zero):
            return False
        return True

    def snoc(self, value: T) -> ImplicitQueue[T]:
        if isinstance(self.que, Shallow):
            if isinstance(self.que.f, Zero):
                return ImplicitQueue(Shallow(One(value)))
            else:
                x = self.que.f.x
                susp = Suspension(lambda: ImplicitQueue())
                return ImplicitQueue[T](Deep(Two(x, value), susp, Zero()))
        else:
            if isinstance(self.que.r, Zero):
                return ImplicitQueue(Deep(self.que.f, self.que.m, One(value)))
            else:
                x = self.que.r.x
                susp = Suspension(lambda: self.que.m.force().snoc((x, value)))
                return ImplicitQueue[T](Deep(self.que.f, susp, Zero()))

    def head(self) -> T:
        if isinstance(self.que.f, Zero):
            raise IndexError("head from empty queue")
        else:
            return self.que.f.x

    def tail(self) -> ImplicitQueue[T]:
        if isinstance(self.que, Shallow):
            if isinstance(self.que.f, Zero):
                raise IndexError("tail from empty queue")
            else:
                return ImplicitQueue[T]()
        else:
            if isinstance(self.que.f, Two):
                y = self.que.f.y
                return ImplicitQueue[T](Deep(One(y), self.que.m, self.que.r))
            else:
                if not self.que.m.force():
                    return ImplicitQueue[T](Shallow(self.que.r))
                else:
                    y, z = self.que.m.force().head()
                    susp = Suspension(lambda: self.que.m.force().tail())
                    return ImplicitQueue[T](Deep(Two(y, z), susp, self.que.r))
