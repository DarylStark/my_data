"""TODO: documentation.
"""
from pytest import fixture
from my_data.my_data import MyData

from my_model.user_scoped_models import User

from sqlmodel import Session, select


def get_user_with_username(my_data: MyData, username: str) -> User | None:
    with Session(my_data.database_engine) as session:
        user = select(User).where(User.username == username)
        query = session.exec(user)
        return query.first()


@fixture
def root_user(my_data: MyData) -> User | None:
    """TODO: documentation. """
    return get_user_with_username(my_data, 'root')


@fixture
def normal_user_1(my_data: MyData) -> User | None:
    """TODO: documentation. """
    return get_user_with_username(my_data, 'normal.user.1')


@fixture
def normal_user_2(my_data: MyData) -> User | None:
    """TODO: documentation. """
    return get_user_with_username(my_data, 'normal.user.2')
