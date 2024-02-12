"""Tests for API scopes."""
# pylint: disable=redefined-outer-name
from pytest import fixture

from my_model import APIScope


@fixture
def example_api_scope() -> APIScope:
    """Fixture that creates a APIScope object.

    Returns:
        The created APIScope object.
    """
    token = APIScope(module='mymodule', subject='mysubject')
    return token


def test_api_scope_full_scope_name(example_api_scope: APIScope) -> None:
    """Unit test to see if the full name is correct.

    Args:
        example_api_scope: a API scope.
    """

    assert example_api_scope.full_scope_name == 'mymodule.mysubject'
