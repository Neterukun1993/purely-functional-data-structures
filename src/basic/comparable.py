from __future__ import annotations
from typing import TypeVar, Protocol, Any


class Comparable(Protocol):
    def __eq__(self, other: Any) -> bool: ...

    def __lt__(self: CT, other: CT) -> bool: ...

    def __le__(self: CT, other: CT) -> bool: ...


CT = TypeVar('CT', bound=Comparable)
