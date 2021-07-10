from __future__ import annotations
from typing import TypeVar, Generic, ClassVar, Dict, Any


T = TypeVar('T')


class MetaSingleton(type, Generic[T]):
    Nil: ClassVar[Dict[MetaSingleton[T], T]] = {}

    def __call__(cls: MetaSingleton[T],  # type: ignore[override]
                 *args: Any) -> T:
        if cls not in cls.Nil:
            cls.Nil[cls] = super().__call__(*args)
        obj: T = super().__call__(*args)
        return cls.Nil[cls] if not args else obj
