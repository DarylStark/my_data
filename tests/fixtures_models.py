"""Module with model fixtures.

This module contains fixtures for specific models from the `my-model` package.
These objects can be used to test with pre-defined values.
"""
from datetime import datetime

from my_model.user_scoped_models import User, UserRole
from pytest import fixture


@fixture
def root_user() -> User:
    """Create a user with root privileges.

    Creates a user with root privileges.

    Returns:
        User: the user that gets created.
    """
    return User(
        id=1,
        fullname='Root',
        username='root',
        email='root@my-daryl-stark.nl',
        role=UserRole.ROOT,
        password_hash='xxx',
        password_date=datetime.now())


@fixture
def normal_user() -> User:
    """Create a user with normal privileges.

    Creates a user with normal privileges.

    Returns:
        User: the user that gets created.
    """
    return User(
        id=2,
        fullname='Daryl Stark',
        username='daryl.stark',
        email='normal@my-daryl-stark.nl',
        role=UserRole.USER,
        password_hash='xxx',
        password_date=datetime.now())
