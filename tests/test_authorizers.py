"""Tests for the APITokenAuthorizer class and it's authorizers."""
# pylint: disable=protected-access
# pylint: disable=unused-argument
import pytest

from my_data import MyData
from my_data.authorizer import APITokenAuthorizer, InvalidTokenAuthorizer, ShortLivedTokenAuthorizer, ValidTokenAuthorizer
from my_data.exceptions import (APITokenAuthorizerAlreadySetException,
                                AuthorizationFailed)


def test_creating_api_token_authorizer(my_data: MyData) -> None:
    """Test creating a APITokenAuthorizer with a Authorizer.

    After doing this, the `_api_token_authorizer` attribute of the authorizer
    should be set to the APITokenAuthorizer.
    """
    invalid_token_authroizer = InvalidTokenAuthorizer()
    api_token_authorizer = APITokenAuthorizer(
        authorizer=invalid_token_authroizer)
    assert (invalid_token_authroizer._api_token_authorizer is
            api_token_authorizer)


def test_setting_api_token_authorizer_again(my_data: MyData) -> None:
    """Test setting a authorizer when it is already set.

    Should raise a APITokenAuthorizerAlreadySetException exception.
    """
    invalid_token_authroizer = InvalidTokenAuthorizer()
    api_token_authorizer = APITokenAuthorizer(
        authorizer=invalid_token_authroizer)

    with pytest.raises(APITokenAuthorizerAlreadySetException):
        invalid_token_authroizer.set_api_token_authorizer(api_token_authorizer)


@pytest.mark.parametrize("api_token", [
    'invalid_token_1', 'invalid_token_2', None
])
def test_invalid_token_authorizer_invalid_token(
        my_data: MyData,
        api_token: str | None
) -> None:
    """Test the InvalidTokenAuthorizer with a invalid token.

    Should not raise an exception since the token is invalid.
    """
    authorizer = APITokenAuthorizer(
        api_token=api_token,
        authorizer=InvalidTokenAuthorizer())
    authorizer.authorize()


@pytest.mark.parametrize("api_token", [
    'aRlIytpyz61JX2TvczLxJZUsRzk578pE'
])
def test_invalid_token_authorizer_valid_token(
        my_data: MyData,
        api_token: str
) -> None:
    """Test the InvalidTokenAuthorizer with a valid token.

    Should raise an exception. A valid token
    """
    authorizer = APITokenAuthorizer(
        api_token=api_token,
        authorizer=InvalidTokenAuthorizer())
    with pytest.raises(AuthorizationFailed):
        authorizer.authorize()


@pytest.mark.parametrize("api_token", [
    'aRlIytpyz61JX2TvczLxJZUsRzk578pE'
])
def test_valid_token_authorizer_valid_token(
        my_data: MyData,
        api_token: str
) -> None:
    """Test the ValidTokenAuthorizer with a valid token.

    Should not raise an exception since the token is valid.
    """
    authorizer = APITokenAuthorizer(
        api_token=api_token,
        authorizer=ValidTokenAuthorizer())
    authorizer.authorize()


@pytest.mark.parametrize("api_token", [
    'invalid_token_1', 'invalid_token_2', None
])
def test_valid_token_authorizer_invalid_token(
        my_data: MyData,
        api_token: str | None
) -> None:
    """Test the ValidTokenAuthorizer with a invalid token.

    Should raise an exception.
    """
    authorizer = APITokenAuthorizer(
        api_token=api_token,
        authorizer=ValidTokenAuthorizer())
    with pytest.raises(AuthorizationFailed):
        authorizer.authorize()


@pytest.mark.parametrize("api_token", [
    'aRlIytpyz61JX2TvczLxJZUsRzk578pE'
])
def test_short_lived_token_authorizer_valid_token(
        my_data: MyData,
        api_token: str
) -> None:
    """Test the ShortLivedTokenAuthorizer with a valid token.

    Should not raise an exception since the token is valid _and_ short lived.
    """
    authorizer = APITokenAuthorizer(
        api_token=api_token,
        authorizer=ShortLivedTokenAuthorizer())
    authorizer.authorize()


@pytest.mark.parametrize("api_token", [
    '2e3n4RSr4I6TnRSwXRpjDYhs9XIYNwhv'
])
def test_short_lived_token_authorizer_long_lived_token(
        my_data: MyData,
        api_token: str
) -> None:
    """Test the ShortLivedTokenAuthorizer with a long lived token.

    Should raise an exception.
    """
    authorizer = APITokenAuthorizer(
        api_token=api_token,
        authorizer=ShortLivedTokenAuthorizer())
    with pytest.raises(AuthorizationFailed):
        authorizer.authorize()
