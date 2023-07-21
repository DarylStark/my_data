"""Unit tests to retrieve data from the database.

This module contains unit tests that retrieve data from the database.
"""

from my_model.user_scoped_models import Tag, User
from sqlmodel import or_

from my_data import MyData


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


def test_data_retrieval_all_api_clients_as_root(
        my_data: MyData, root_user: User) -> None:
    """Test API Client retrieval as a ROOT user.

    Retrieves API clients from the database as a root user. Should retrieve
    only API clients for his own account.

    Args:
        my_data: a instance to a MyData object.
        root_user: the root user for the context.
    """
    with my_data.get_context(user=root_user) as context:
        api_clients = context.api_clients.retrieve()
        assert len(api_clients) == 3
        assert api_clients[0].app_name == 'root_api_client_1'
        assert api_clients[0].app_publisher == 'root_api_client_1_publisher'
        assert api_clients[1].app_name == 'root_api_client_2'
        assert api_clients[1].app_publisher == 'root_api_client_2_publisher'
        assert api_clients[2].app_name == 'root_api_client_3'
        assert api_clients[2].app_publisher == 'root_api_client_3_publisher'


def test_data_retrieval_all_api_clients_as_normal_user_1(
        my_data: MyData, normal_user_1: User) -> None:
    """Test API Client retrieval as a USER user.

    Retrieves API Clients from the database as a normal user. Should retrieve
    only API Client for his own account.

    Args:
        my_data: a instance to a MyData object.
        normal_user_1: the first normal user.
    """
    with my_data.get_context(user=normal_user_1) as context:
        api_clients = context.api_clients.retrieve()
        assert len(api_clients) == 3
        assert api_clients[0].app_name == 'normal_user_1_api_client_1'
        assert (api_clients[0].app_publisher ==
                'normal_user_1_api_client_1_publisher')
        assert api_clients[1].app_name == 'normal_user_1_api_client_2'
        assert (api_clients[1].app_publisher ==
                'normal_user_1_api_client_2_publisher')
        assert api_clients[2].app_name == 'normal_user_1_api_client_3'
        assert (api_clients[2].app_publisher ==
                'normal_user_1_api_client_3_publisher')


def test_data_retrieval_all_api_clients_as_normal_user_2(
        my_data: MyData, normal_user_2: User) -> None:
    """Test API client retrieval as a USER user.

    Retrieves API Clients from the database as a normal user. Should retrieve
    only API Client for his own account.

    Args:
        my_data: a instance to a MyData object.
        normal_user_2: the second normal user.
    """
    with my_data.get_context(user=normal_user_2) as context:
        api_clients = context.api_clients.retrieve()
        assert len(api_clients) == 3
        assert api_clients[0].app_name == 'normal_user_2_api_client_1'
        assert (api_clients[0].app_publisher ==
                'normal_user_2_api_client_1_publisher')
        assert api_clients[1].app_name == 'normal_user_2_api_client_2'
        assert (api_clients[1].app_publisher ==
                'normal_user_2_api_client_2_publisher')
        assert api_clients[2].app_name == 'normal_user_1_api_client_3'
        assert (api_clients[2].app_publisher ==
                'normal_user_2_api_client_3_publisher')


def test_data_retrieval_all_api_tokens_as_root(
        my_data: MyData, root_user: User) -> None:
    """Test API Token retrieval as a ROOT user.

    Retrieves API token from the database as a root user. Should retrieve
    only API tokens for his own account.

    Args:
        my_data: a instance to a MyData object.
        root_user: the root user for the context.
    """
    with my_data.get_context(user=root_user) as context:
        api_tokens = context.api_tokens.retrieve()
        assert len(api_tokens) == 3
        assert api_tokens[0].title == 'root_api_token_1'
        assert api_tokens[1].title == 'root_api_token_2'
        assert api_tokens[2].title == 'root_api_token_3'


def test_data_retrieval_all_api_tokens_as_normal_user_1(
        my_data: MyData, normal_user_1: User) -> None:
    """Test API Token retrieval as a USER user.

    Retrieves API tokens from the database as a normal user. Should retrieve
    only API tokens for his own account.

    Args:
        my_data: a instance to a MyData object.
        normal_user_1: the first normal user.
    """
    with my_data.get_context(user=normal_user_1) as context:
        api_tokens = context.api_tokens.retrieve()
        assert len(api_tokens) == 3
        assert api_tokens[0].title == 'normal_user_1_api_token_1'
        assert api_tokens[1].title == 'normal_user_1_api_token_2'
        assert api_tokens[2].title == 'normal_user_1_api_token_3'


def test_data_retrieval_all_api_tokens_as_normal_user_2(
        my_data: MyData, normal_user_2: User) -> None:
    """Test API tokens retrieval as a USER user.

    Retrieves API tokens from the database as a normal user. Should retrieve
    only API tokens for his own account.

    Args:
        my_data: a instance to a MyData object.
        normal_user_2: the second normal user.
    """
    with my_data.get_context(user=normal_user_2) as context:
        api_tokens = context.api_tokens.retrieve()
        assert len(api_tokens) == 3
        assert api_tokens[0].title == 'normal_user_2_api_token_1'
        assert api_tokens[1].title == 'normal_user_2_api_token_2'
        assert api_tokens[2].title == 'normal_user_2_api_token_3'


def test_data_retrieval_all_web_ui_settings_as_root(
        my_data: MyData, root_user: User) -> None:
    """Test Web UI setting retrieval as a ROOT user.

    Retrieves Web UI settings from the database as a root user. Should retrieve
    only Web UI settings for his own account.

    Args:
        my_data: a instance to a MyData object.
        root_user: the root user for the context.
    """
    with my_data.get_context(user=root_user) as context:
        web_ui_settings = context.web_ui_settings.retrieve()
        assert len(web_ui_settings) == 3
        assert web_ui_settings[0].setting == 'root_test_setting_1'
        assert web_ui_settings[1].setting == 'root_test_setting_2'
        assert web_ui_settings[2].setting == 'root_test_setting_3'


def test_data_retrieval_all_web_ui_settings_as_normal_user_1(
        my_data: MyData, normal_user_1: User) -> None:
    """Test Web UI setting retrieval as a USER user.

    Retrieves Web UI settings from the database as a normal user. Should
    retrieve only Web UI settings for his own account.

    Args:
        my_data: a instance to a MyData object.
        normal_user_1: the first normal user.
    """
    with my_data.get_context(user=normal_user_1) as context:
        web_ui_settings = context.web_ui_settings.retrieve()
        assert len(web_ui_settings) == 3
        assert web_ui_settings[0].setting == 'normal_user_1_test_setting_1'
        assert web_ui_settings[1].setting == 'normal_user_1_test_setting_2'
        assert web_ui_settings[2].setting == 'normal_user_1_test_setting_3'


def test_data_retrieval_all_web_ui_settings_as_normal_user_2(
        my_data: MyData, normal_user_2: User) -> None:
    """Test Web UI setting retrieval as a USER user.

    Retrieves Web UI settings from the database as a normal user. Should
    retrieve only Web UI settings for his own account.

    Args:
        my_data: a instance to a MyData object.
        normal_user_2: the second normal user.
    """
    with my_data.get_context(user=normal_user_2) as context:
        web_ui_settings = context.web_ui_settings.retrieve()
        assert len(web_ui_settings) == 3
        assert web_ui_settings[0].setting == 'normal_user_2_test_setting_1'
        assert web_ui_settings[1].setting == 'normal_user_2_test_setting_2'
        assert web_ui_settings[2].setting == 'normal_user_2_test_setting_3'
