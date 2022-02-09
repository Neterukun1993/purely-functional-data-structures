from __future__ import annotations
from typing import *
from src.basic.meta_singleton import MetaSingleton


T = TypeVar('T')
StreamPair = Tuple[T, 'Stream[T]']
StreamCell = Union[None, Callable[[], StreamPair[T]], StreamPair[T]]


class Stream(Generic[T], metaclass=MetaSingleton):
    def __init__(self, stream_cell: StreamCell[T] = None) -> None:
        self.stream_cell = stream_cell

    def __bool__(self) -> bool:
        return self is not Stream()

    def __iter__(self) -> Iterator[T]:
        ptr = self
        while ptr:
            yield ptr.head()
            ptr = ptr.tail()

    def cons(self, value: T) -> Stream[T]:
        return Stream((value, self))

    def head(self) -> T:
        if callable(self.stream_cell):
            self.stream_cell = self.stream_cell()
        return cast(StreamPair[T], self.stream_cell)[0]

    def tail(self) -> Stream[T]:
        if callable(self.stream_cell):
            self.stream_cell = self.stream_cell()
        return cast(StreamPair[T], self.stream_cell)[1]

    def concat(self, other: Stream[T]) -> Stream[T]:
        if not self:
            return other
        func = lambda: (self.head(), self.tail().concat(other))
        return Stream(func)

    def reverse(self) -> Stream[T]:
        def func() -> StreamPair[T]:
            ret = Stream[T]()
            for x in self:
                ret = ret.cons(x)
            return cast(StreamPair[T], ret.stream_cell)
        return Stream(func)

    def take(self, n: int) -> Stream[T]:
        if n == 0 or not self:
            return Stream()
        func = lambda: (self.head(), self.tail().take(n - 1))
        return Stream(func)

    def drop(self, n: int) -> Stream[T]:
        def func() -> StreamPair[T]:
            ret = self
            for _ in range(n):
                if not ret:
                    break
                ret = ret.tail()
            if ret:
                ret.tail()
            return cast(StreamPair[T], ret.stream_cell)
        return Stream(func)
