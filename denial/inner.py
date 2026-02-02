from itertools import count
from typing import Any, Optional, Union

from printo import descript_data_object, not_none


class InnerNoneType:
    id: Optional[Union[int, str]]  # pragma: no cover
    auto: bool  # pragma: no cover
    counter = count()

    def __init__(self, id: Optional[Union[int, str]] = None, doc: Optional[str] = None, auto: bool = False) -> None:  # noqa: A002
        if id is None:
            self.id = next(self.counter)
            self.auto = True
        else:
            self.id = id
            self.auto = auto
        self.doc = doc

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, type(self)):
            return False
        return self.id == other.id and self.auto == other.auto

    def __hash__(self) -> int:
        return hash(self.id)

    def __repr__(self) -> str:
        if self.id == 0 and self.auto:
            return 'InnerNone'
        return descript_data_object(type(self).__name__, (self.id,), {'doc': self.doc, 'auto': self.auto}, filters={'auto': lambda x: x != True, 'doc': not_none})

    def __bool__(self) -> bool:
        return False


InnerNone = InnerNoneType()
