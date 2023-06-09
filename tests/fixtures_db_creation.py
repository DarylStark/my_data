from datetime import datetime

from my_model.user import UserRole
from pytest import fixture

from database.database import Database
from database.factories import create_memory_sqlite_database
from my_data.db_connection import db_connection
from my_data.db_models import DBTag, DBUser


@fixture
def db() -> Database:
    # Create a connection to the in-memory database
    create_memory_sqlite_database(db_connection)

    # Create the tables
    db_connection.create_tables(drop_tables=False)

    with db_connection.get_session() as a:
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
    return db_connection
