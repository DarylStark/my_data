"""Unit tests to test the tasks for Service users.

This module tests the things a Service user needs to do, like retrieving
User objects or API tokens.
"""

from my_model.user_scoped_models import User, APIToken

from my_data.my_data import MyData


def test_retrieving_user_objects(my_data: MyData) -> None:
    """Unit test to retrieve a User object using a Service user.

    This unit test tries to log in with a Service user and retrieve a User
    object using the username and password for the user. This can be used by
    clients that need a user to login.
    """
    with my_data.get_context_for_service_user(
            username='service.user',
            password='service_password') as context:
        user = context.users.retrieve(User.username == 'normal.user.1')
        assert len(user) == 1
        assert user[0].verify_credentials('normal.user.1', 'normal_user_1_pw')


def test_retrieving_api_tokens(my_data: MyData) -> None:
    """Unit test to retrieve a User object using a API token.

    This unit test tries to log in with a Service user and retrieve a User
    object using a given API token. This can be used, for instance, by a
    REST API service to retrieve the correct user for given API token.
    """
    with my_data.get_context_for_service_user(
            username='service.user',
            password='service_password') as context:
        token = context.api_tokens.retrieve(
            APIToken.token == 'normal_user_2_api_token_1')
        assert len(token) == 1
        assert (token[0].user.username == 'normal.user.2')
