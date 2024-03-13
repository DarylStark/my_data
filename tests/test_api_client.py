"""Tests for API Client objects."""

import pytest
from my_model import APIClient
from pytest import fixture, raises


@fixture
def example_api_client() -> APIClient:
    """Fixture that creates a APIClient object.

    Returns:
        The created APIClient object.
    """
    client = APIClient(app_name='testapp', app_publisher='Daryl Stark')
    return client


@pytest.mark.parametrize(
    'token',
    ['abcdefghijklmnopqrstuvwxyz', 'xyz', 'qwertyuiopASDFGHJKLzxcvbnm--909'],
)
def test_api_client_invalid_token_regex(
    example_api_client: APIClient, token: str
) -> None:
    """Unit test to test invalid tokens.

    Args:
        example_api_client: a API client to test.
        token: the token to test.
    """
    with raises(ValueError):
        example_api_client.token = token


@pytest.mark.parametrize('token', ['qwertyuiopASDFGHJKLzxcvbnm009909'])
def test_api_client_valid_token_regex(
    example_api_client: APIClient, token: str
) -> None:
    """Unit test to test valid tokens.

    Args:
        example_api_client: a API client to test.
        token: the token to test.
    """
    example_api_client.token = token


@pytest.mark.parametrize(
    'url',
    ['http:/example.com/api?redirect=1', 'https:/example.com/api?redirect=1'],
)
def test_api_client_invalid_url_regex(
    example_api_client: APIClient, url: str
) -> None:
    """Unit test to test invalid URLs.

    Args:
        example_api_client: a API client to test.
        url: the URL to test.
    """
    with raises(ValueError):
        example_api_client.redirect_url = url


@pytest.mark.parametrize(
    'url',
    [
        'http://example.com/api?redirect=1',
        'https://example.com/api?redirect=1',
    ],
)
def test_api_client_valid_url_regex(
    example_api_client: APIClient, url: str
) -> None:
    """Unit test to test valid URLs.

    Args:
        example_api_client: a API client to test.
        url: the URL to test.
    """
    example_api_client.redirect_url = url


def test_api_client_random_token(example_api_client: APIClient) -> None:
    """Unit test to see if we can set a random token.

    Args:
        example_api_client: a API client to test.
    """
    # Set a random token for the API token
    token = example_api_client.set_random_token()
    assert token == example_api_client.token


def test_api_client_overwrite(example_api_client: APIClient) -> None:
    """Test if we can overwrite the token with Force.

    Args:
        example_api_client: a API client to test.
    """
    token = example_api_client.set_random_token()
    new_token = example_api_client.set_random_token(force=True)
    assert token != new_token


def test_api_client_not_overwrite(example_api_client: APIClient) -> None:
    """Test if we get an error when we try to overwrite the token.

    Args:
        example_api_client: a API client to test.
    """
    _ = example_api_client.set_random_token()
    with raises(PermissionError):
        _ = example_api_client.set_random_token()
