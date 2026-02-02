import pytest

from denial import InnerNone, InnerNoneType, SentinelType


@pytest.mark.mypy_testing
def test_sentinel_is_including_inner_none_and_just_none():
    variable: SentinelType = InnerNone  # noqa: F841
    another_variable: SentinelType = None  # noqa: F841


@pytest.mark.mypy_testing
def test_sentinel_is_including_inner_none_type():
    variable: SentinelType = InnerNoneType()  # noqa: F841
    another_variable: SentinelType = InnerNoneType(123)  # noqa: F841
    another_else_variable: SentinelType = InnerNoneType('kek')  # noqa: F841

    class InheritorInnerNoneType(InnerNoneType):
        ...

    another_another_else_variable: SentinelType = InheritorInnerNoneType()  # noqa: F841


@pytest.mark.mypy_testing
def test_wrong_using_of_sentinel():
    variable: SentinelType = 123 # E: [assignment] # noqa: F841
    another_variable: SentinelType = 'kek' # E: [assignment] # noqa: F841
    another_else_variable: SentinelType = False # E: [assignment] # noqa: F841
