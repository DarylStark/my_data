"""Tests for the APITokenAuthorizer class and it's authorizers."""
# pylint: disable=protected-access
# pylint: disable=unused-argument
import pytest
from my_model import UserRole

from my_data import MyData
from my_data.authorizer import (APIScopeAuthorizer, APITokenAuthorizer,
                                InvalidTokenAuthorizer,
                                ShortLivedTokenAuthorizer,
                                ValidTokenAuthorizer)
from my_data.exceptions import (APITokenAuthorizerAlreadySetException,
                                AuthorizationFailed)


def test_creating_api_token_authorizer(my_data: MyData) -> None:
    """Test creating a APITokenAuthorizer with a Authorizer.

    After doing this, the `_api_token_authorizer` attribute of the authorizer
    should be set to the APITokenAuthorizer.

    Args:
        my_data: a instance to a MyData object.
    """
    invalid_token_authroizer = InvalidTokenAuthorizer()
    api_token_authorizer = APITokenAuthorizer(
        authorizer=invalid_token_authroizer)
    assert (invalid_token_authroizer._api_token_authorizer is
            api_token_authorizer)


def test_setting_api_token_authorizer_again(my_data: MyData) -> None:
    """Test setting a authorizer when it is already set.

    Should raise a APITokenAuthorizerAlreadySetException exception.

    Args:
        my_data: a instance to a MyData object.
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
        api_token: str | None) -> None:
    """Test the InvalidTokenAuthorizer with a invalid token.

    Should not raise an exception since the token is invalid.

    Args:
        my_data: a instance to a MyData object.
        api_token: a API token to test.
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

    Should raise an exception.

    Args:
        my_data: a instance to a MyData object.
        api_token: a API token to test.
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

    Args:
        my_data: a instance to a MyData object.
        api_token: a API token to test.
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

    Args:
        my_data: a instance to a MyData object.
        api_token: a API token to test.
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

    Args:
        my_data: a instance to a MyData object.
        api_token: a API token to test.
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

    Args:
        my_data: a instance to a MyData object.
        api_token: a API token to test.
    """
    authorizer = APITokenAuthorizer(
        api_token=api_token,
        authorizer=ShortLivedTokenAuthorizer())
    with pytest.raises(AuthorizationFailed):
        authorizer.authorize()


def test_api_token_authorizer_get_api_token_empty_user(
    my_data: MyData
) -> None:
    """Test `_get_api_token` with an empty user.

    Args:
        my_data: a instance to a MyData object.
    """
    authorizer = APITokenAuthorizer(
        authorizer=ShortLivedTokenAuthorizer())
    assert authorizer._get_api_token() is None


def test_api_token_authorizer_get_api_token_invalid_token(
    my_data: MyData
) -> None:
    """Test `_get_api_token` with an a invalid token.

    Args:
        my_data: a instance to a MyData object.
    """
    authorizer = APITokenAuthorizer(
        api_token='invalid_token',
        authorizer=ShortLivedTokenAuthorizer())
    assert authorizer._get_api_token() is None


@pytest.mark.parametrize("api_token", [
    'aRlIytpyz61JX2TvczLxJZUsRzk578pE'
])
def test_api_token_authorizer_get_user_role(
        my_data: MyData,
        api_token: str) -> None:
    """Test retrieving the User Role from the API Token.

    Args:
        my_data: a instance to a MyData object.
        api_token: a API token to test.
    """
    authorizer = APITokenAuthorizer(
        api_token=api_token,
        authorizer=ShortLivedTokenAuthorizer())
    user_role = authorizer._get_user_role()
    assert user_role is UserRole.USER


def test_api_token_authorizer_get_user_role_invalid_token(
        my_data: MyData) -> None:
    """Test retrieving the User Role from the API Token.

    Args:
        my_data: a instance to a MyData object.
    """
    authorizer = APITokenAuthorizer(
        api_token='invalid_token',
        authorizer=ShortLivedTokenAuthorizer())
    user_role = authorizer._get_user_role()
    assert user_role is None


@pytest.mark.parametrize("api_token", [
    'aRlIytpyz61JX2TvczLxJZUsRzk578pE'
])
def test_api_token_authorizer_is_valid_user(
        my_data: MyData,
        api_token: str) -> None:
    """Test checking is_valid_user property.

    Args:
        my_data: a instance to a MyData object.
        api_token: a API token to test.
    """
    authorizer = APITokenAuthorizer(
        api_token=api_token,
        authorizer=ShortLivedTokenAuthorizer())
    assert authorizer.is_valid_user is True


def test_api_token_authorizer_is_valid_user_invalid_token(
        my_data: MyData) -> None:
    """Test checking is_valid_user property.

    Args:
        my_data: a instance to a MyData object.
    """
    authorizer = APITokenAuthorizer(
        api_token='invalid_token',
        authorizer=ShortLivedTokenAuthorizer())
    assert authorizer.is_valid_user is False


@pytest.mark.parametrize("api_token", [
    'aRlIytpyz61JX2TvczLxJZUsRzk578pE'
])
def test_api_token_authorizer_is_root(
        my_data: MyData,
        api_token: str) -> None:
    """Test checking is_root property.

    Args:
        my_data: a instance to a MyData object.
        api_token: a API token to test.
    """
    authorizer = APITokenAuthorizer(
        api_token=api_token,
        authorizer=ShortLivedTokenAuthorizer())
    assert authorizer.is_root is False


@pytest.mark.parametrize("api_token", [
    'aRlIytpyz61JX2TvczLxJZUsRzk578pE'
])
def test_api_token_authorizer_is_normal_user(
        my_data: MyData,
        api_token: str) -> None:
    """Test checking is_normal_user property.

    Args:
        my_data: a instance to a MyData object.
        api_token: a API token to test.
    """
    authorizer = APITokenAuthorizer(
        api_token=api_token,
        authorizer=ShortLivedTokenAuthorizer())
    assert authorizer.is_normal_user is True


@pytest.mark.parametrize("api_token", [
    'aRlIytpyz61JX2TvczLxJZUsRzk578pE'
])
def test_api_token_authorizer_is_service_user(
        my_data: MyData,
        api_token: str) -> None:
    """Test checking is_service_user property.

    Args:
        my_data: a instance to a MyData object.
        api_token: a API token to test.
    """
    authorizer = APITokenAuthorizer(
        api_token=api_token,
        authorizer=ShortLivedTokenAuthorizer())
    assert authorizer.is_service_user is False


@pytest.mark.parametrize("api_token", [
    'aRlIytpyz61JX2TvczLxJZUsRzk578pE'
])
def test_api_token_authorizer_is_short_lived(
        my_data: MyData,
        api_token: str) -> None:
    """Test checking is_short_lived_token property with a short lived token.

    Args:
        my_data: a instance to a MyData object.
        api_token: a API token to test.
    """
    authorizer = APITokenAuthorizer(
        api_token=api_token,
        authorizer=ShortLivedTokenAuthorizer())
    assert authorizer.is_short_lived_token is True


@pytest.mark.parametrize("api_token", [
    '2e3n4RSr4I6TnRSwXRpjDYhs9XIYNwhv', None
])
def test_api_token_authorizer_is_short_lived_invalid_token(
        my_data: MyData,
        api_token: str) -> None:
    """Test checking is_short_lived_token property with a long lived token.

    Args:
        my_data: a instance to a MyData object.
        api_token: a API token to test.
    """
    authorizer = APITokenAuthorizer(
        api_token=api_token,
        authorizer=ShortLivedTokenAuthorizer())
    assert authorizer.is_short_lived_token is False


@pytest.mark.parametrize("api_token", [
    'aRlIytpyz61JX2TvczLxJZUsRzk578pE', None
])
def test_api_token_authorizer_is_long_lived(
        my_data: MyData,
        api_token: str) -> None:
    """Test checking is_long_lived_token property with a short lived token.

    Args:
        my_data: a instance to a MyData object.
        api_token: a API token to test.
    """
    authorizer = APITokenAuthorizer(
        api_token=api_token,
        authorizer=ShortLivedTokenAuthorizer())
    assert authorizer.is_long_lived_token is False


@pytest.mark.parametrize("api_token", [
    '2e3n4RSr4I6TnRSwXRpjDYhs9XIYNwhv'
])
def test_api_token_authorizer_is_long_lived_invalid_token(
        my_data: MyData,
        api_token: str) -> None:
    """Test checking is_long_lived_token property with a long lived token.

    Args:
        my_data: a instance to a MyData object.
        api_token: a API token to test.
    """
    authorizer = APITokenAuthorizer(
        api_token=api_token,
        authorizer=ShortLivedTokenAuthorizer())
    assert authorizer.is_long_lived_token is True


@pytest.mark.parametrize("api_token", [
    'MHxHL4HrmmJHbAR1b0gV4OkpuEsxxmRL',
    None
])
def test_disabled_token(
        my_data: MyData,
        api_token: str) -> None:
    """Test checking is_enabled property.

    Args:
        my_data: a instance to a MyData object.
        api_token: a API token to test.
    """
    authorizer = APITokenAuthorizer(
        api_token=api_token)
    assert authorizer.is_enabled is False


@pytest.mark.parametrize("api_token", [
    'Cbxfv44aNlWRMu4bVqawWu9vofhFWmED',
    None
])
def test_expired_token(
        my_data: MyData,
        api_token: str) -> None:
    """Test checking is_not_expired property.

    Args:
        my_data: a instance to a MyData object.
        api_token: a API token to test.
    """
    authorizer = APITokenAuthorizer(
        api_token=api_token)
    assert authorizer.is_not_expired is False


@pytest.mark.parametrize("api_token", [
    'aRlIytpyz61JX2TvczLxJZUsRzk578pE',
])
def test_api_scope_authorizer_short_lived(
        my_data: MyData,
        api_token: str) -> None:
    """Test the API scope authorizer on short lived tokens.

    Should always be a success if the token is correct since short lived tokens
    don't work with API scopes and we don't specify that short lived tokens
    should fail.

    Args:
        my_data: a instance to a MyData object.
        api_token: a API token to test.
    """
    authorizer = APITokenAuthorizer(
        api_token=api_token,
        authorizer=APIScopeAuthorizer(
            required_scopes=['users.retrieve', 'users.create']
        ))
    authorizer.authorize()


@pytest.mark.parametrize("api_token", [
    '2e3n4RSr4I6TnRSwXRpjDYhs9XIYNwhv',
])
def test_api_scope_authorizer_long_lived(
        my_data: MyData,
        api_token: str) -> None:
    """Test the scope authorizer on long lived tokens with the needed scopes.

    Should be successful since the given long lived tokens have the needed
    scopes.

    Args:
        my_data: a instance to a MyData object.
        api_token: a API token to test.
    """
    authorizer = APITokenAuthorizer(
        api_token=api_token,
        authorizer=APIScopeAuthorizer(
            required_scopes=['users.retrieve', 'users.create']
        ))
    authorizer.authorize()


@pytest.mark.parametrize("api_token", [
    'aRlIytpyz61JX2TvczLxJZUsRzk578pE',
])
def test_api_scope_authorizer_short_lived_not_allowed(
        my_data: MyData,
        api_token: str) -> None:
    """Test the API scope authorizer on short lived tokens without permissions.

    Should fail since we are telling the authorizer to fail for short lived
    tokens.

    Args:
        my_data: a instance to a MyData object.
        api_token: a API token to test.
    """
    authorizer = APITokenAuthorizer(
        api_token=api_token,
        authorizer=APIScopeAuthorizer(
            required_scopes=['users.retrieve', 'users.create'],
            allow_short_lived=False
        ))
    with pytest.raises(AuthorizationFailed):
        authorizer.authorize()


@pytest.mark.parametrize("api_token", [
    'BynORM5FVkt07BuQSA09lQUIrgCgOqEv',
])
def test_api_scope_authorizer_long_lived_not_allowed(
        my_data: MyData,
        api_token: str) -> None:
    """Test the scope authorizer on long lived tokens without needed scopes.

    Should fail since the given long lived tokens don't have the needed scopes.

    Args:
        my_data: a instance to a MyData object.
        api_token: a API token to test.
    """
    authorizer = APITokenAuthorizer(
        api_token=api_token,
        authorizer=APIScopeAuthorizer(
            required_scopes=['users.retrieve', 'users.create']
        ))
    with pytest.raises(AuthorizationFailed):
        authorizer.authorize()


@pytest.mark.parametrize("api_token", [
    'BynORM5FVkt07BuQSA09lQUIrgCgOqEv',
])
def test_api_scope_authorizer_long_lived_partially_not_allowed(
        my_data: MyData,
        api_token: str) -> None:
    """Test the scope authorizer on long lived tokens without needed scopes.

    Should fail since the given long lived tokens don't have the needed scopes.
    The difference with `test_api_scope_authorizer_long_lived_not_allowed` is
    that we test here if the auhorizer fails when only one of the scopes is
    missing.

    Args:
        my_data: a instance to a MyData object.
        api_token: a API token to test.
    """
    authorizer = APITokenAuthorizer(
        api_token=api_token,
        authorizer=APIScopeAuthorizer(
            required_scopes=['users.retrieve', 'users.delete']
        ))
    with pytest.raises(AuthorizationFailed):
        authorizer.authorize()
