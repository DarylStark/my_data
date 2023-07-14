"""Unit tests to retrieve data from the database.

This module contains unit tests that retrieve data from the database.
"""

from my_data import MyData
from my_model.user_scoped_models import User, Tag
from sqlmodel import or_


def test_data_retrieval_all_users_as_root(
        my_data: MyData, root_user: User) -> None:
    """Test User retrieval as a ROOT user.

    Retrieves Users from the database as a root user. Should retrieve all
    users.

    Args:
        my_data: a instance to a MyData object.
        root_user: the root user for the context.
    """
    with my_data.get_context(user=root_user) as context:
        users = context.users.retrieve()
        assert users[0].username == 'root'
        assert users[1].username == 'normal.user.1'
        assert users[2].username == 'normal.user.2'


def test_data_retrieval_filtered_users_as_root(
        my_data: MyData, root_user: User) -> None:
    """Test User retrieval as a ROOT user with a filter.

    Retrieves Users from the database as a root user with a filter. Should
    retrieve two users.

    Args:
        my_data: a instance to a MyData object.
        root_user: the root user for the context.
    """
    with my_data.get_context(user=root_user) as context:
        users = context.users.retrieve(
            or_(User.username == 'normal.user.2', User.username == 'root'))
        assert len(users) == 2
        assert users[0].username == 'root'
        assert users[1].username == 'normal.user.2'


def test_data_retrieval_all_users_as_normal_user_1(
        my_data: MyData, normal_user_1: User) -> None:
    """Test User retrieval as a USER user.

    Retrieves Users from the database as a normal user. Should retrieve only
    his own account.

    Args:
        my_data: a instance to a MyData object.
        normal_user_1: the first normal user.
    """
    with my_data.get_context(user=normal_user_1) as context:
        users = context.users.retrieve()
        assert len(users) == 1
        assert users[0].username == 'normal.user.1'


def test_data_retrieval_all_users_as_normal_user_2(
        my_data: MyData, normal_user_2: User) -> None:
    """Test User retrieval as a USER user.

    Retrieves Users from the database as a normal user. Should retrieve only
    his own account.

    Args:
        my_data: a instance to a MyData object.
        normal_user_2: the second normal user.
    """
    with my_data.get_context(user=normal_user_2) as context:
        users = context.users.retrieve()
        assert len(users) == 1
        assert users[0].username == 'normal.user.2'


def test_data_retrieval_all_tags_as_root(
        my_data: MyData, root_user: User) -> None:
    """Test Tag retrieval as a ROOT user.

    Retrieves Tags from the database as a root user. Should retrieve only
    tags for his own account.

    Args:
        my_data: a instance to a MyData object.
        root_user: the root user for the context.
    """
    with my_data.get_context(user=root_user) as context:
        tags = context.tags.retrieve()
        assert len(tags) == 3
        assert tags[0].title == 'root_tag_1'
        assert tags[1].title == 'root_tag_2'
        assert tags[2].title == 'root_tag_3'


def test_data_retrieval_all_tags_as_normal_user_1(
        my_data: MyData, normal_user_1: User) -> None:
    """Test Tag retrieval as a USER user.

    Retrieves Tags from the database as a normal user. Should retrieve only
    tags for his own account.

    Args:
        my_data: a instance to a MyData object.
        normal_user_1: the first normal user.
    """
    with my_data.get_context(user=normal_user_1) as context:
        tags = context.tags.retrieve()
        assert len(tags) == 3
        assert tags[0].title == 'normal_user_1_tag_1'
        assert tags[1].title == 'normal_user_1_tag_2'
        assert tags[2].title == 'normal_user_1_tag_3'


def test_data_retrieval_all_tags_as_normal_user_2(
        my_data: MyData, normal_user_2: User) -> None:
    """Test Tag retrieval as a USER user.

    Retrieves Tags from the database as a normal user. Should retrieve only
    tags for his own account.

    Args:
        my_data: a instance to a MyData object.
        normal_user_2: the second normal user.
    """
    with my_data.get_context(user=normal_user_2) as context:
        tags = context.tags.retrieve()
        assert len(tags) == 3
        assert tags[0].title == 'normal_user_2_tag_1'
        assert tags[1].title == 'normal_user_2_tag_2'
        assert tags[2].title == 'normal_user_2_tag_3'


def test_data_retrieval_filtered_tags_as_normal_user_1(
        my_data: MyData, normal_user_1: User) -> None:
    """Test Tag retrieval as a USER user with a filter.

    Retrieves Tags from the database as a normal user with a filter. Should
    retrieve only tags for his own account that comply to the filter.

    Args:
        my_data: a instance to a MyData object.
        normal_user_1: the first normal user.
    """
    with my_data.get_context(user=normal_user_1) as context:
        tags = context.tags.retrieve(Tag.title == 'normal_user_1_tag_2')
        assert len(tags) == 1
        assert tags[0].title == 'normal_user_1_tag_2'
