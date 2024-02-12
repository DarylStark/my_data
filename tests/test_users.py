"""Tests for User objects."""
# pylint: disable=redefined-outer-name
from datetime import datetime

from pyotp import TOTP
from pytest import fixture, raises
import pytest

from my_model import User


@fixture
def example_user_no_second_factor() -> User:
    """Fixture that creates a User object.

    Returns:
        The created User object.
    """
    user = User(
        created=datetime.utcnow(),
        fullname='Fake fullname',
        username='fake.user',
        email='fakse@fake.example',
        password_hash='xxxxx',
        password_date=datetime.utcnow(),
        second_factor=None)
    user.set_password('testtest')
    return user


def test_user_fullname_regex(example_user_no_second_factor: User) -> None:
    """Unit test to check if fullnames that are invalid fail.

    Args:
        example_user_no_second_factor: a user without a second factor.
    """

    # List with wrong full names
    wrong_full_names = [
        '', 'Daryl_Stark', 'Emilia_Clarke'
    ]

    # Loop through them and make sure they fail
    for wrong_username in wrong_full_names:
        with raises(ValueError):
            example_user_no_second_factor.fullname = wrong_username

    # Test correct username
    example_user_no_second_factor.fullname = 'Daryl Stark'
    example_user_no_second_factor.fullname = 'Emilia Clarke'
    example_user_no_second_factor.fullname = 'Emilia-Clarke'
    example_user_no_second_factor.fullname = 'Daryl Stark 1'


def test_user_username_regex(example_user_no_second_factor: User) -> None:
    """Unit test to check if usernames that are invalid fail.

    Args:
        example_user_no_second_factor: a user without a second factor.
    """

    # List with wrong usernames
    wrong_usernames = [
        '', 'user name', 'user+name',
        'user@domain.example', '1username', '_username',
        '-username'
    ]

    # Loop through them and make sure they fail
    for wrong_username in wrong_usernames:
        with raises(ValueError):
            example_user_no_second_factor.username = wrong_username

    # Test correct username
    example_user_no_second_factor.username = 'daryl.stark'
    example_user_no_second_factor.username = 'emilia.clarke'
    example_user_no_second_factor.username = 'emilia_clarke'


@pytest.mark.parametrize('wrong_address', ['', 'fake_mail', 'daryl@daryl'])
def test_user_wrong_email_regex(
        example_user_no_second_factor: User,
        wrong_address: str) -> None:
    """Unit test to check if emailaddresses that are invalid fail.

    Args:
        example_user_no_second_factor: a user without a second factor.
        wrong_address: the email address to test.
    """
    with raises(ValueError):
        example_user_no_second_factor.email = wrong_address


@pytest.mark.parametrize('correct_address',
                         ['daryl.stark@dstark.nl',
                          'emilia.clarke@dstark.nl',
                          'emilia_clarke@dstark.co.uk'])
def test_user_correct_email_regex(
        example_user_no_second_factor: User,
        correct_address: str) -> None:
    """Unit test to check if emailaddresses that are valid don't fail.

    Args:
        example_user_no_second_factor: a user without a second factor.
        correct_address: the email address to test.
    """
    # Test correct username
    example_user_no_second_factor.email = correct_address


@pytest.mark.parametrize('wrong_second_factor', ['ape', 'daryl', '123ape'])
def test_user_wrong_second_factor_regex(
        example_user_no_second_factor: User,
        wrong_second_factor: str) -> None:
    """Unit test to check if second factors that are invalid fail.

    Args:
        example_user_no_second_factor: a user without a second factor.
        wrong_second_factor: the second factor to test.
    """

    with raises(ValueError):
        example_user_no_second_factor.second_factor = wrong_second_factor


@pytest.mark.parametrize('second_factor', ['ABCDEFG', '123ABCEF', 'HIJKLMN'])
def test_user_correct_second_factor_regex(
        example_user_no_second_factor: User,
        second_factor: str) -> None:
    """Test correct second factors.

    Args:
        example_user_no_second_factor: a user without a second factor.
        second_factor: the second factor to test.
    """
    example_user_no_second_factor.second_factor = second_factor


def test_user_correct_credentials(example_user_no_second_factor: User) -> None:
    """Test if credentials can be set and verified.

    Args:
        example_user_no_second_factor: a user without a second factor.
    """

    # Test username/password combination
    assert example_user_no_second_factor.verify_credentials(
        username='fake.user',
        password='testtest'), 'Credential verification failed (without ' + \
        ' second factor)'

    # Create a OTP for the user
    otp_secret = example_user_no_second_factor.set_random_second_factor()

    # Test username/password/second factor combination
    assert example_user_no_second_factor.verify_credentials(
        username='fake.user',
        password='testtest',
        second_factor=TOTP(otp_secret).now()), "Credential verification ' + \
            'failed (with second factor)"


def test_disabling_second_factor(example_user_no_second_factor: User) -> None:
    """Test if we can disable the second factor.

    Args:
        example_user_no_second_factor: a user without a second factor.
    """
    # Create a OTP for the user
    otp_secret = example_user_no_second_factor.set_random_second_factor()
    assert otp_secret is not None
    example_user_no_second_factor.disable_second_factor()
    assert example_user_no_second_factor.second_factor is None


def test_user_incorrect_credentials(
        example_user_no_second_factor: User) -> None:
    """Test if wrong credentials result in error.

    Args:
        example_user_no_second_factor: a user without a second factor.
    """

    # Test username/password combination
    assert not example_user_no_second_factor.verify_credentials(
        username='fake.user',
        password='somethingelse'), "Credential didn't fail when they ' + \
            'should've (without second factor)"

    # Create a OTP for the user
    _ = example_user_no_second_factor.set_random_second_factor()

    # Test username/password/second factor combination
    assert not example_user_no_second_factor.verify_credentials(
        username='fake.user',
        password='testtest',
        second_factor='alsowrong'), "Credential didn't fail when they ' + \
            'should've (with second factor)"


def test_user_no_password(example_user_no_second_factor: User) -> None:
    """Test wrong credentials if no password is set.

    Args:
        example_user_no_second_factor: a user without a second factor.
    """
    example_user_no_second_factor.password_hash = None
    assert not example_user_no_second_factor.verify_credentials(
        username='fake.user',
        password='testtest')
