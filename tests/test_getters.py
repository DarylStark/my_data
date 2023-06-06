from pytest import fixture

from my_data.db_connection import _db_connection
from my_data.context import Context
from database.database import Database
from my_data.db_models import DBTag, DBUser, UserRole
from my_model.user import User
from datetime import datetime
from sqlmodel import Session, select


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


@fixture
def db() -> Database:
    # Create a connection to the in-memory database
    _db_connection.configure('sqlite:///:memory:')
    _db_connection.create_engine()

    # Create the tables
    _db_connection.create_tables(drop_tables=False)

    with _db_connection.get_session() as a:
        # Root user
        root = DBUser(
            fullname='Root',
            username='root',
            email='root@dstark.nl',
            role=UserRole.ROOT,
            password_hash='asdasdas',
            password_date=datetime.now())
        root.tags = [
            DBTag(title='test_root_1'),
            DBTag(title='test_root_2'),
        ]
        a.add(root)

        # User for Daryl Stark
        daryl = DBUser(
            fullname='Daryl Stark',
            username='daryl.stark',
            email='daryl@dstark.nl',
            role=UserRole.USER,
            password_hash='asdasdas',
            password_date=datetime.now())
        daryl.tags = [
            DBTag(title='test_daryl_1'),
            DBTag(title='test_daryl_2')
        ]
        a.add(daryl)

        a.commit()

    # Return the connection object
    return _db_connection


def test_tags(db: Database, normal_user: User) -> None:
    with Context(user=normal_user) as c:
        tags = c.tags.get()
        assert tags[0].title == 'test_daryl_1'
        assert tags[1].title == 'test_daryl_2'


def test_get_users_normal(db: Database, normal_user: User) -> None:
    with Context(user=normal_user) as c:
        users = c.users.get()
        assert (users[0].username == 'daryl.stark')
        assert (len(users) == 1)


def test_get_users_root(db: Database, root_user: User) -> None:
    with Context(user=root_user) as c:
        users = c.users.get()
        assert (users[0].username == 'root')
        assert (users[1].username == 'daryl.stark')
        assert (len(users) == 2)
