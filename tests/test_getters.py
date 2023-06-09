from my_model.user import User

from database.database import Database
from my_data.context import Context


def test_tags(db: Database, normal_user: User, pytestconfig) -> None:
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
