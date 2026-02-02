from itertools import count
from threading import Lock
from typing import Any, Optional, Union

from printo import descript_data_object, not_none
from locklib import ContextLockProtocol

from denial.errors import (
    DoubleSingletonsInstantiationError,
    SingletonMarkConflictError,
)


class InnerNoneType:
    id: Optional[Union[int, str]]  # pragma: no cover
    auto: bool  # pragma: no cover
    is_singleton: bool = False
    has_instances: bool = False
    counter = count()
    lock: ContextLockProtocol = Lock()

    def __init__(self, id: Optional[Union[int, str]] = None, doc: Optional[str] = None, auto: bool = False) -> None:  # noqa: A002
        if id is None:
            self.id = next(self.counter)
            self.auto = True
        else:
            self.id = id
            self.auto = auto

        self.doc = doc

        if self.is_singleton:
            with self.lock:
                if self.has_instances:
                    raise DoubleSingletonsInstantiationError(f'Class "{type(self).__name__}" is marked with a flag prohibiting the creation of more than one instance.')
                type(self).has_instances = True
        else:
            type(self).has_instances = True

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

    def __init_subclass__(cls, singleton: bool = False):
        if getattr(cls.__mro__[1], 'is_singleton', False) and not singleton:
            raise SingletonMarkConflictError('An inheritor of a singleton class cannot be declared a non-singleton.')

        super().__init_subclass__()

        cls.is_singleton = singleton
        cls.has_instances = False


InnerNone = InnerNoneType()
