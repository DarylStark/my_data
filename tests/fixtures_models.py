from datetime import datetime

from my_model.user import User, UserRole
from pytest import fixture


@fixture
def root_user() -> User:
    return User(
        id=1,
        fullname='Root',
        username='root',
        email='root@dstark.nl',
        role=UserRole.ROOT,
        password_hash='asdasdas',
        password_date=datetime.now())


@fixture
def normal_user() -> User:
    return User(
        id=2,
        fullname='Daryl Stark',
        username='daryl.stark',
        email='daryl@dstark.nl',
        role=UserRole.USER,
        password_hash='asdasdas',
        password_date=datetime.now())
