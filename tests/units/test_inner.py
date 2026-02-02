from threading import Thread
from typing import cast

import pytest
from full_match import match

from denial import InnerNone, InnerNoneType
from denial.errors import (
    DoubleSingletonsInstantiationError,
    SingletonMarkConflictError,
)


def test_inner_none_is_inner_none():
    assert InnerNone is InnerNone  # noqa: PLR0124


def test_inner_none_is_instance_of_inner_none_type():
    assert isinstance(InnerNone, InnerNoneType)


def test_str_inner_none():
    assert str(InnerNone) == 'InnerNone'


def test_repr_inner_none():
    assert repr(InnerNone) == 'InnerNone'


def test_new_instance_has_id_more_0():
    instance_1 = InnerNoneType()
    instance_2 = InnerNoneType()

    assert isinstance(instance_1.id, int)
    assert isinstance(instance_2.id, int)

    assert InnerNone.id == 0
    assert instance_1.id > 0
    assert instance_2.id > 0
    assert instance_2.id == instance_1.id + 1


def test_inheritor_ids():
    instance = InnerNoneType()

    class InheritorInnerNoneType(InnerNoneType):
        ...

    inheritors_instance = InheritorInnerNoneType()

    assert cast(int, inheritors_instance.id) > cast(int, instance.id)
    assert cast(int, inheritors_instance.id) < cast(int, InheritorInnerNoneType().id)


def test_new_instance_repr():
    class InheritorInnerNoneType(InnerNoneType):
        ...

    assert InnerNoneType.__name__ == 'InnerNoneType'
    assert InheritorInnerNoneType.__name__ == 'InheritorInnerNoneType'

    for class_object in (InnerNoneType, InheritorInnerNoneType):
        class_name = class_object.__name__
        new_instance = class_object()
        new_instance_with_doc = class_object(doc='lol')

        assert repr(new_instance) == f'{class_name}({new_instance.id})'
        assert repr(class_object('kek')) == f"{class_name}('kek', auto=False)"
        assert repr(class_object(123)) == f"{class_name}(123, auto=False)"
        assert repr(class_object(0)) == f"{class_name}(0, auto=False)"

        assert repr(new_instance_with_doc) == f"{class_name}({new_instance_with_doc.id}, doc='lol')"
        assert repr(class_object('kek', doc='lol')) == f"{class_name}('kek', doc='lol', auto=False)"
        assert repr(class_object(123, doc='lol')) == f"{class_name}(123, doc='lol', auto=False)"
        assert repr(class_object(0, doc='lol')) == f"{class_name}(0, doc='lol', auto=False)"

        assert repr(class_object('', auto=True)) != 'InnerNone'
        assert class_name in repr(class_object('', auto=True))


def test_eq():
    new_instance = InnerNoneType()

    assert InnerNone == InnerNone  # noqa: PLR0124
    assert InnerNone != new_instance
    assert InnerNone != InnerNoneType('kek')
    assert InnerNone != InnerNoneType(123)

    assert new_instance == new_instance  # noqa: PLR0124
    assert new_instance != InnerNoneType()
    assert InnerNoneType() != InnerNoneType()

    assert InnerNoneType(123) == InnerNoneType(123)
    assert InnerNoneType('kek') == InnerNoneType('kek')

    assert InnerNoneType(123) != InnerNoneType(124)
    assert InnerNoneType('kek') != InnerNoneType(123)
    assert InnerNoneType('kek') != InnerNoneType('lol')

    assert InnerNone != None  # noqa: E711
    assert InnerNoneType() != None  # noqa: E711
    assert InnerNoneType(123) != None  # noqa: E711

    assert InnerNoneType(123) != 123
    assert InnerNoneType('kek') != 'kek'


def test_hashing_and_use_as_key_in_dict():
    assert hash(InnerNone) == hash(InnerNone.id)
    assert hash(InnerNoneType(123)) == hash(123)
    assert hash(InnerNoneType('123')) == hash('123')

    new_instance = InnerNoneType()
    assert hash(new_instance) == hash(new_instance.id)

    dict_with_it = {new_instance: 'kek'}
    assert dict_with_it[new_instance] == 'kek'

    another_instance = InnerNoneType()

    dict_with_both = {new_instance: 'kek', another_instance: 'lol'}

    assert dict_with_both[new_instance] == 'kek'
    assert dict_with_both[another_instance] == 'lol'

    dict_with_named_ids = {InnerNoneType('kek'): 'kek', InnerNoneType('lol'): 'lol'}

    assert dict_with_named_ids[InnerNoneType('kek')] == 'kek'
    assert dict_with_named_ids[InnerNoneType('lol')] == 'lol'

    dict_with_integer_ids = {InnerNoneType(123): 123, InnerNoneType(1234): 1234}

    assert dict_with_integer_ids[InnerNoneType(123)] == 123
    assert dict_with_integer_ids[InnerNoneType(1234)] == 1234


def test_thread_safety():
    number_of_iterations = 10_000
    number_of_threads = 10

    nones = []

    def go_increment():
        for _ in range(number_of_iterations):
            nones.append(InnerNoneType())

    threads = [Thread(target=go_increment) for _ in range(number_of_threads)]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    assert len(set(x.id for x in nones)) == number_of_iterations * number_of_threads


def test_bool():
    assert not bool(None)
    assert not bool(InnerNone)
    assert not bool(InnerNoneType())
    assert not bool(InnerNoneType(0))
    assert not bool(InnerNoneType(123))
    assert not bool(InnerNoneType('kek'))


def test_auto_flag():
    assert InnerNone != InnerNoneType(0)

    instance = InnerNoneType()

    assert InnerNoneType(instance.id) != instance

def test_i_can_use_auto_flag_manually():
    assert InnerNoneType(0, auto=True) == InnerNone

    instance = InnerNoneType()

    assert InnerNoneType(instance.id, auto=True) == instance


def test_inheritor_singleton_double_usage():
    class LocalInheritor(InnerNoneType, singleton=True):
        ...

    LocalInheritor()

    with pytest.raises(DoubleSingletonsInstantiationError, match=match('Class "LocalInheritor" is marked with a flag prohibiting the creation of more than one instance.')):
        LocalInheritor()


def test_inheritor_not_singleton_double_usage():
    class AnotherLocalInheritor(InnerNoneType):
        ...

    first_instance = AnotherLocalInheritor()
    second_instance = AnotherLocalInheritor()

    assert cast(int, second_instance.id) > cast(int, first_instance.id)


def test_try_to_inherit_singleton_class_with_singleton_mark():
    class FirstLocalInheritor(InnerNoneType, singleton=True):
        ...

    class SecondLocalInheritor(FirstLocalInheritor, singleton=True):
        ...


def test_try_to_inherit_singleton_class_with_no_singleton_mark():
    class FirstLocalInheritor(InnerNoneType, singleton=True):
        ...

    with pytest.raises(SingletonMarkConflictError, match=match('An inheritor of a singleton class cannot be declared a non-singleton.')):
        class SecondLocalInheritor(FirstLocalInheritor, singleton=False):
            ...

    with pytest.raises(SingletonMarkConflictError, match=match('An inheritor of a singleton class cannot be declared a non-singleton.')):
        class AnotherSecondLocalInheritor(FirstLocalInheritor, singleton=False):
            ...


def test_independence_of_singleton_marks():
    class FirstLocalInheritor(InnerNoneType, singleton=True):
        ...

    FirstLocalInheritor()

    class SecondLocalInheritor(FirstLocalInheritor, singleton=True):
        ...

    SecondLocalInheritor()

    with pytest.raises(DoubleSingletonsInstantiationError, match=match('Class "SecondLocalInheritor" is marked with a flag prohibiting the creation of more than one instance.')):
        SecondLocalInheritor()
