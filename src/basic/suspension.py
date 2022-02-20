from typing import TypeVar, Generic, Callable, Union


T = TypeVar('T')


class Suspension(Generic[T]):
    func: Union[T, Callable[[], T]]

    def __init__(self, func: Callable[[], T]) -> None:
        self.func = func

    def force(self) -> T:
        if callable(self.func):
            self.func = self.func()
        return self.func
