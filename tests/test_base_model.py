"""Tests for the Base Model."""
# pylint: disable=redefined-outer-name

import pytest
from my_model import MyModel


@pytest.mark.parametrize(
    'min_value, max_value', [(1, 10), (2, 20), (25, 30), (50, 100)]
)
def test_base_model_get_random_token(min_value: int, max_value: int) -> None:
    """Unit test to test the `get_random_token` method.

    Args:
        min_value: the minimum password length.
        max_value: the maximum password length.
    """
    model = MyModel()
    random_string = model.get_random_string(
        min_length=min_value, max_length=max_value, include_punctation=True
    )
    assert len(random_string) >= min_value
    assert len(random_string) <= max_value
