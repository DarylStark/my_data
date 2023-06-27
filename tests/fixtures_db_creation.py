"""Module with DB creation fixtures.

Contains the fixture to connect to a database and create the needed tables for
the unit tests.
"""
from my_model.tag import Tag
from my_model.user import User
from pytest import fixture

from database.database import Database
from my_data.configure import DatabaseType, MyDataConfig, configure
from my_data.context import Context


@fixture
def db(root_user: User, normal_user: User) -> Database:
    """Fixture to connect to the DB.

    Creates the database connection and creates the tables. For the unit tests
    we use a SQLite database.

    Returns:
        Database: the database connection
    """
    # Create a connection to the in-memory database
    db_connection = configure(MyDataConfig(
        db_type=DatabaseType.SQLITE_MEMORY
    ))

    # Create the tables
    db_connection.create_tables(drop_tables=False)

    # Create the users. We use the object of the root user for this
    # with Context(user=root_user) as local_context:
    #     local_context.users.create([root_user, normal_user])
    #     local_context.tags.create([
    #         Tag(title='root_tag_1'),
    #         Tag(title='root_tag_2')])

    # # Create tags for the normal user
    # with Context(user=normal_user) as local_context:
    #     local_context.tags.create([
    #         Tag(title='test_daryl_1'),
    #         Tag(title='test_daryl_2')])

    t1 = Tag(title='test_daryl_1', color=None, user=normal_user)
    t2 = Tag(title='test_daryl_2', color=None, user=normal_user)

    with db_connection.get_session(expire_on_commit=False) as s:
        s.add(root_user)
        s.add(normal_user)
        s.add(t1)
        s.add(t2)
        s.commit()

    # Return the connection object
    return db_connection
