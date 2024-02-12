"""Tests for API Tokens."""
# pylint: disable=redefined-outer-name
from pytest import fixture, raises
import pytest

from my_model import APIToken


@fixture
def example_api_token() -> APIToken:
    """Fixture that creates a APIToken object.

    Returns:
        The created APIToken object.
    """
    token = APIToken(title='testtoken')
    return token


@pytest.mark.parametrize(
    'token',
    [
        'abcdefghijklmnopqrstuvwxyz',
        'xyz',
        'qwertyuiopASDFGHJKLzxcvbnm--909'
    ]
)
def test_api_token_wrong_token_regex(
    example_api_token: APIToken,
    token: str
) -> None:
    """Unit test to test invalid tokens.

    Args:
        example_api_token: a API token to test.
        token: the token to test.
    """

    # Invalid tokens
    with raises(ValueError):
        example_api_token.token = token


@pytest.mark.parametrize(
    'token',
    ['qwertyuiopASDFGHJKLzxcvbnm009909']
)
def test_api_token_token_regex(
    example_api_token: APIToken,
    token: str
) -> None:
    """Unit test to test valid tokens.

    Args:
        example_api_token: a API token to test.
        token: the token to test.
    """

    # Valid tokens
    example_api_token.token = token


def test_api_token_random_token(example_api_token: APIToken) -> None:
    """Unit test to see if we can set a random token.

    Args:
        example_api_token: a API token to test.
    """

    # Set a random token for the API Token
    token = example_api_token.set_random_token()
    assert token == example_api_token.token


def test_api_token_overwrite(example_api_token: APIToken) -> None:
    """Test if we can overwrite the token with Force.

    Args:
        example_api_token: a API token to test.
    """

    token = example_api_token.set_random_token()
    new_token = example_api_token.set_random_token(force=True)
    assert token != new_token


def test_api_token_not_overwrite(example_api_token: APIToken) -> None:
    """Test if we get an error when we try to overwrite the token.

    Args:
        example_api_token: a API token to test.
    """

    _ = example_api_token.set_random_token()
    with raises(PermissionError):
        _ = example_api_token.set_random_token()
