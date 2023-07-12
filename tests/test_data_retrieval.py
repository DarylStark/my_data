"""TODO: documentation. """

from my_data.my_data import MyData
from my_model.user_scoped_models import User


def test_data_retrieval_all_users_as_root(
        my_data: MyData, root_user: User) -> None:
    """TODO: documentation. """
    with my_data.get_context(user=root_user) as context:
        users = context.users.retrieve()
        assert len(users) == 3
        assert users[0].username == 'root'
        assert users[1].username == 'normal.user.1'
        assert users[2].username == 'normal.user.2'


def test_data_retrieval_all_users_as_normal_user_1(
        my_data: MyData, normal_user_1: User) -> None:
    """TODO: documentation. """
    with my_data.get_context(user=normal_user_1) as context:
        users = context.users.retrieve()
        assert len(users) == 1
        assert users[0].username == 'normal.user.1'


def test_data_retrieval_all_users_as_normal_user_2(
        my_data: MyData, normal_user_2: User) -> None:
    """TODO: documentation. """
    with my_data.get_context(user=normal_user_2) as context:
        users = context.users.retrieve()
        assert len(users) == 1
        assert users[0].username == 'normal.user.2'
