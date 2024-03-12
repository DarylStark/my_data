"""Unit tests to retrieve data from the database.

This module contains unit tests that retrieve data from the database.
"""
# pylint: disable=redefined-outer-name

import pytest
from my_data import MyData
from my_model import APIToken, Tag, User
from sqlmodel import or_
from sqlmodel.sql.expression import desc


@pytest.mark.parametrize(
    'index, username',
    [
        (0, 'root'),
        (1, 'normal.user.1'),
        (2, 'normal.user.2'),
        (3, 'service.user'),
    ],
)
def test_data_retrieval_all_users_as_root(
    my_data: MyData, root_user: User, index: int, username: str
) -> None:
    """Test User retrieval as a ROOT user.

    Retrieves Users from the database as a root user. Should retrieve all
    users.

    Args:
        my_data: a instance to a MyData object.
        root_user: the root user for the context.
        index: the user index.
        username: the username.
    """
    with my_data.get_context(user=root_user) as context:
        users = context.users.retrieve()
        assert users[index].username == username


@pytest.mark.parametrize(
    'index, username', [(0, 'normal.user.2'), (1, 'root')]
)
def test_data_retrieval_filtered_users_as_root(
    my_data: MyData, root_user: User, index: int, username: str
) -> None:
    """Test User retrieval as a ROOT user with a filter.

    Retrieves Users from the database as a root user with a filter. Should
    retrieve two users.

    Args:
        my_data: a instance to a MyData object.
        root_user: the service user for the context.
        index: test index.
        username: test username.
    """
    with my_data.get_context(user=root_user) as context:
        users = context.users.retrieve(
            or_(User.username == 'normal.user.2', User.username == 'root')
        )
        assert len(users) == 2
        assert users[index].username == username


def test_data_retrieval_all_users_as_normal_user_1(
    my_data: MyData, normal_user_1: User
) -> None:
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
    my_data: MyData, normal_user_2: User
) -> None:
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


@pytest.mark.parametrize(
    'index, title', [(0, 'root_tag_1'), (1, 'root_tag_2'), (2, 'root_tag_3')]
)
def test_data_retrieval_all_tags_as_root(
    my_data: MyData, root_user: User, index: int, title: str
) -> None:
    """Test Tag retrieval as a ROOT user.

    Retrieves Tags from the database as a root user. Should retrieve only
    tags for his own account.

    Args:
        my_data: a instance to a MyData object.
        root_user: the root user for the context.
        index: the user index.
        title: the title.
    """
    with my_data.get_context(user=root_user) as context:
        tags = context.tags.retrieve()
        assert len(tags) == 3
        assert tags[index].title == title


@pytest.mark.parametrize(
    'index, title',
    [
        (0, 'normal_user_1_tag_1'),
        (1, 'normal_user_1_tag_2'),
        (2, 'normal_user_1_tag_3'),
    ],
)
def test_data_retrieval_all_tags_as_normal_user_1(
    my_data: MyData, normal_user_1: User, index: int, title: str
) -> None:
    """Test Tag retrieval as a USER user.

    Retrieves Tags from the database as a normal user. Should retrieve only
    tags for his own account.

    Args:
        my_data: a instance to a MyData object.
        normal_user_1: the first normal user.
        index: the user index.
        title: the title.
    """
    with my_data.get_context(user=normal_user_1) as context:
        tags = context.tags.retrieve()
        assert len(tags) == 3
        assert tags[index].title == title


@pytest.mark.parametrize(
    'index, title',
    [
        (0, 'normal_user_2_tag_1'),
        (1, 'normal_user_2_tag_2'),
        (2, 'normal_user_2_tag_3'),
    ],
)
def test_data_retrieval_all_tags_as_normal_user_2(
    my_data: MyData, normal_user_2: User, index: int, title: str
) -> None:
    """Test Tag retrieval as a USER user.

    Retrieves Tags from the database as a normal user. Should retrieve only
    tags for his own account.

    Args:
        my_data: a instance to a MyData object.
        normal_user_2: the second normal user.
        index: test index.
        title: test title.
    """
    with my_data.get_context(user=normal_user_2) as context:
        tags = context.tags.retrieve()
        assert len(tags) == 3
        assert tags[index].title == title


@pytest.mark.parametrize(
    'index, title',
    [
        (0, 'normal_user_2_tag_3'),
        (1, 'normal_user_2_tag_2'),
        (2, 'normal_user_2_tag_1'),
    ],
)
def test_data_retrieval_all_tags_as_normal_user_2_reverse_sort(
    my_data: MyData, normal_user_2: User, index: int, title: str
) -> None:
    """Test Tag retrieval as a USER user and sort it reversed on title.

    Retrieves Tags from the database as a normal user and sort it on title
    reversed. This way, we can test the sorting.

    Args:
        my_data: a instance to a MyData object.
        normal_user_2: the second normal user.
        index: test index.
        title: test title.
    """
    with my_data.get_context(user=normal_user_2) as context:
        tags = context.tags.retrieve(sort=desc(Tag.title))
        assert len(tags) == 3
        assert tags[index].title == title


@pytest.mark.parametrize(
    'start, title',
    [
        (0, 'normal_user_2_tag_1'),
        (1, 'normal_user_2_tag_2'),
        (2, 'normal_user_2_tag_3'),
    ],
)
def test_data_retrieval_all_tags_as_normal_user_2_paginated(
    my_data: MyData, normal_user_2: User, start: int, title: str
) -> None:
    """Test Tag retrieval as a USER user and do it one by one.

    Retrieves Tags from the database as a normal user and specify to only
    retrieve one item each time in a new page. This way, we can test the
    pagination.

    Args:
        my_data: a instance to a MyData object.
        normal_user_2: the second normal user.
        start: the start to test.
        title: test title.
    """
    with my_data.get_context(user=normal_user_2) as context:
        tags = context.tags.retrieve(start=start, max_items=1)
        assert len(tags) == 1
        assert tags[0].title == title


def test_data_retrieval_filtered_tags_as_normal_user_1(
    my_data: MyData, normal_user_1: User
) -> None:
    """Test Tag retrieval as a USER user with a filter.

    Retrieves Tags from the database as a normal user with a filter. Should
    retrieve only tags for his own account that comply to the filter.

    Args:
        my_data: a instance to a MyData object.
        normal_user_1: the first normal user.
    """
    with my_data.get_context(user=normal_user_1) as context:
        tags = context.tags.retrieve(
            Tag.title  # type:ignore
            == 'normal_user_1_tag_2'
        )
        assert len(tags) == 1
        assert tags[0].title == 'normal_user_1_tag_2'


@pytest.mark.parametrize(
    'index, app_name, app_publisher',
    [
        (0, 'root_api_client_1', 'root_api_client_1_publisher'),
        (1, 'root_api_client_2', 'root_api_client_2_publisher'),
        (2, 'root_api_client_3', 'root_api_client_3_publisher'),
    ],
)
def test_data_retrieval_all_api_clients_as_root(
    my_data: MyData,
    root_user: User,
    index: int,
    app_name: str,
    app_publisher: str,
) -> None:
    """Test API Client retrieval as a ROOT user.

    Retrieves API clients from the database as a root user. Should retrieve
    only API clients for his own account.

    Args:
        my_data: a instance to a MyData object.
        root_user: the root user for the context.
        index: test index.
        app_name: test app name.
        app_publisher: test app publisher.
    """
    with my_data.get_context(user=root_user) as context:
        api_clients = context.api_clients.retrieve()
        assert len(api_clients) == 3
        assert api_clients[index].app_name == app_name
        assert api_clients[index].app_publisher == app_publisher


@pytest.mark.parametrize(
    'index, app_name, app_publisher',
    [
        (
            0,
            'normal_user_1_api_client_1',
            'normal_user_1_api_client_1_publisher',
        ),
        (
            1,
            'normal_user_1_api_client_2',
            'normal_user_1_api_client_2_publisher',
        ),
        (
            2,
            'normal_user_1_api_client_3',
            'normal_user_1_api_client_3_publisher',
        ),
    ],
)
def test_data_retrieval_all_api_clients_as_normal_user_1(
    my_data: MyData,
    normal_user_1: User,
    index: int,
    app_name: str,
    app_publisher: str,
) -> None:
    """Test API Client retrieval as a USER user.

    Retrieves API Clients from the database as a normal user. Should retrieve
    only API Client for his own account.

    Args:
        my_data: a instance to a MyData object.
        normal_user_1: the first normal user.
        index: test index.
        app_name: test app name.
        app_publisher: test app publisher.
    """
    with my_data.get_context(user=normal_user_1) as context:
        api_clients = context.api_clients.retrieve()
        assert len(api_clients) == 3
        assert api_clients[index].app_name == app_name
        assert api_clients[index].app_publisher == app_publisher


@pytest.mark.parametrize(
    'index, app_name, app_publisher',
    [
        (
            0,
            'normal_user_2_api_client_1',
            'normal_user_2_api_client_1_publisher',
        ),
        (
            1,
            'normal_user_2_api_client_2',
            'normal_user_2_api_client_2_publisher',
        ),
        (
            2,
            'normal_user_2_api_client_3',
            'normal_user_2_api_client_3_publisher',
        ),
    ],
)
def test_data_retrieval_all_api_clients_as_normal_user_2(
    my_data: MyData,
    normal_user_2: User,
    index: int,
    app_name: str,
    app_publisher: str,
) -> None:
    """Test API client retrieval as a USER user.

    Retrieves API Clients from the database as a normal user. Should retrieve
    only API Client for his own account.

    Args:
        my_data: a instance to a MyData object.
        normal_user_2: the second normal user.
        index: test index.
        app_name: test app name.
        app_publisher: test app publisher.
    """
    with my_data.get_context(user=normal_user_2) as context:
        api_clients = context.api_clients.retrieve()
        assert len(api_clients) == 3
        assert api_clients[index].app_name == app_name
        assert api_clients[index].app_publisher == app_publisher


@pytest.mark.parametrize(
    'index, title',
    [
        (0, 'root_api_token_1'),
        (1, 'root_api_token_2'),
        (2, 'root_api_token_3'),
    ],
)
def test_data_retrieval_all_api_tokens_as_root(
    my_data: MyData, root_user: User, index: int, title: str
) -> None:
    """Test API Token retrieval as a ROOT user.

    Retrieves API token from the database as a root user. Should retrieve
    only API tokens for his own account.

    Args:
        my_data: a instance to a MyData object.
        root_user: the root user for the context.
        index: test index.
        title: test title.
    """
    with my_data.get_context(user=root_user) as context:
        api_tokens = context.api_tokens.retrieve()
        assert len(api_tokens) == 3
        assert api_tokens[index].title == title


@pytest.mark.parametrize(
    'index, title',
    [
        (0, 'normal_user_1_api_token_1'),
        (1, 'normal_user_1_api_token_2'),
        (2, 'normal_user_1_api_token_3'),
    ],
)
def test_data_retrieval_all_api_tokens_as_normal_user_1(
    my_data: MyData, normal_user_1: User, index: int, title: str
) -> None:
    """Test API Token retrieval as a USER user.

    Retrieves API tokens from the database as a normal user. Should retrieve
    only API tokens for his own account.

    Args:
        my_data: a instance to a MyData object.
        normal_user_1: the first normal user.
        index: test index.
        title: test title.
    """
    with my_data.get_context(user=normal_user_1) as context:
        api_tokens = context.api_tokens.retrieve()
        assert len(api_tokens) == 3
        assert api_tokens[index].title == title


@pytest.mark.parametrize(
    'index, title',
    [
        (0, 'normal_user_2_api_token_1'),
        (1, 'normal_user_2_api_token_2'),
        (2, 'normal_user_2_api_token_3'),
    ],
)
def test_data_retrieval_all_api_tokens_as_normal_user_2(
    my_data: MyData, normal_user_2: User, index: int, title: str
) -> None:
    """Test API tokens retrieval as a USER user.

    Retrieves API tokens from the database as a normal user. Should retrieve
    only API tokens for his own account.

    Args:
        my_data: a instance to a MyData object.
        normal_user_2: the second normal user.
        index: test index.
        title: test title.
    """
    with my_data.get_context(user=normal_user_2) as context:
        api_tokens = context.api_tokens.retrieve(sort=APIToken.title)  # type:ignore
        assert len(api_tokens) == 3
        assert api_tokens[index].title == title


@pytest.mark.parametrize(
    'index, setting',
    [
        (0, 'root_test_setting_1'),
        (1, 'root_test_setting_2'),
        (2, 'root_test_setting_3'),
    ],
)
def test_data_retrieval_all_user_settings_as_root(
    my_data: MyData, root_user: User, index: int, setting: str
) -> None:
    """Test User Setting retrieval as a ROOT user.

    Retrieves User Settings from the database as a root user. Should retrieve
    only User Settings for his own account.

    Args:
        my_data: a instance to a MyData object.
        root_user: the root user for the context.
        index: test index.
        setting: test setting.
    """
    with my_data.get_context(user=root_user) as context:
        user_settings = context.user_settings.retrieve()
        assert len(user_settings) == 3
        assert user_settings[index].setting == setting


@pytest.mark.parametrize(
    'index, setting',
    [
        (0, 'normal_user_1_test_setting_1'),
        (1, 'normal_user_1_test_setting_2'),
        (2, 'normal_user_1_test_setting_3'),
    ],
)
def test_data_retrieval_all_user_settings_as_normal_user_1(
    my_data: MyData, normal_user_1: User, index: int, setting: str
) -> None:
    """Test User Setting retrieval as a USER user.

    Retrieves User Settings from the database as a normal user. Should
    retrieve only User Settings for his own account.

    Args:
        my_data: a instance to a MyData object.
        normal_user_1: the first normal user.
        index: test index.
        setting: test setting.
    """
    with my_data.get_context(user=normal_user_1) as context:
        user_settings = context.user_settings.retrieve()
        assert len(user_settings) == 3
        assert user_settings[index].setting == setting


@pytest.mark.parametrize(
    'index, setting',
    [
        (0, 'normal_user_2_test_setting_1'),
        (1, 'normal_user_2_test_setting_2'),
        (2, 'normal_user_2_test_setting_3'),
    ],
)
def test_data_retrieval_all_user_settings_as_normal_user_2(
    my_data: MyData, normal_user_2: User, index: int, setting: str
) -> None:
    """Test User Setting retrieval as a USER user.

    Retrieves User Settings from the database as a normal user. Should
    retrieve only User Settings for his own account.

    Args:
        my_data: a instance to a MyData object.
        normal_user_2: the second normal user.
        index: test index.
        setting: test setting.
    """
    with my_data.get_context(user=normal_user_2) as context:
        user_settings = context.user_settings.retrieve()
        assert len(user_settings) == 3
        assert user_settings[index].setting == setting


def test_data_count_retrieval_all_tags_as_normal_user_1(
    my_data: MyData, normal_user_1: User
) -> None:
    """Test Tag count retrieval as a USER user.

    Checks how many tags are in the database as a normal user.

    Args:
        my_data: a instance to a MyData object.
        normal_user_1: the second normal user.
    """
    with my_data.get_context(user=normal_user_1) as context:
        tag_count = context.tags.count()
        assert tag_count == 3


def test_data_count_retrieval_all_tags_as_normal_user_2(
    my_data: MyData, normal_user_2: User
) -> None:
    """Test Tag count retrieval as a USER user.

    Checks how many tags are in the database as a normal user.

    Args:
        my_data: a instance to a MyData object.
        normal_user_2: the second normal user.
    """
    with my_data.get_context(user=normal_user_2) as context:
        tag_count = context.tags.count()
        assert tag_count == 3
