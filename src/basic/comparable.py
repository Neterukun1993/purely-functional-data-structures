from __future__ import annotations
from typing import TypeVar, Protocol, Any


class Comparable(Protocol):
    def __eq__(self, other: Any) -> bool: ...

    def __lt__(self: T, other: T) -> bool: ...

    def __le__(self: T, other: T) -> bool: ...


T = TypeVar('T', bound=Comparable)
