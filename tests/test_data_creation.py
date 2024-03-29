"""Unit tests to create data in the database.

This module contains unit tests that create data in the database. After the
creation, it checks if the data has been created.
"""
# pylint: disable=no-member # disabled for the `like` method of Pydantic
# fields.

from my_data import MyData
from my_data.exceptions import PermissionDeniedError
from my_model import APIClient, APIToken, Tag, User, UserSetting
from my_model.model import TemporaryToken, TemporaryTokenType
from pytest import raises
from sqlalchemy.exc import IntegrityError


def test_data_creation_users_as_root(
    my_data: MyData,
    root_user: User,
    test_root_user: User,
    test_normal_user: User,
) -> None:
    """Test User creation as a ROOT user.

    Creates a user as a root user.

    Args:
        my_data: a instance of a MyData object.
        root_user: the root user for the context.
        test_root_user: a ROOT user to create.
        test_normal_user: a USER user to create.
    """
    with my_data.get_context(user=root_user) as context:
        # Create the users.
        context.users.create([test_root_user, test_normal_user])

        # Check if they exist
        created_users = context.users.retrieve(
            User.username.like('creation_test_%')  # type:ignore
        )

        assert len(created_users) == 2
        assert created_users[0].username == 'creation_test_root_user_1'
        assert created_users[1].username == 'creation_test_user_user_1'


def test_data_creation_user_as_service_account(
    my_data: MyData, service_user: User, test_normal_user: User
) -> None:
    """Test User creation as a SERVICE user.

    Creates a user as a service user. This should fail: service users are not
    allowed to create users.

    Args:
        my_data: a instance of a MyData object.
        service_user: the service user.
        test_normal_user: a USER user to create.
    """
    with (
        raises(PermissionDeniedError),
        my_data.get_context(user=service_user) as context,
    ):
        context.users.create(test_normal_user)


def test_data_creation_users_as_normal_user_1(
    my_data: MyData, normal_user_1: User, test_normal_user: User
) -> None:
    """Test User creation as a USER user.

    Creates a user as a normal user. This should fail: normal users are not
    allowed to create users.

    Args:
        my_data: a instance of a MyData object.
        normal_user_1: the first normal user.
        test_normal_user: a USER user to create.
    """
    with (
        raises(PermissionDeniedError),
        my_data.get_context(user=normal_user_1) as context,
    ):
        context.users.create(test_normal_user)


def test_data_creation_users_as_normal_user_2(
    my_data: MyData, normal_user_2: User, test_normal_user: User
) -> None:
    """Test User creation as a USER user.

    Creates a user as a normal user. This should fail: normal users are not
    allowed to create users.

    Args:
        my_data: a instance of a MyData object.
        normal_user_2: the first normal user.
        test_normal_user: a USER user to create.
    """
    with (
        raises(PermissionDeniedError),
        my_data.get_context(user=normal_user_2) as context,
    ):
        context.users.create(test_normal_user)


def test_data_creation_tags_as_root(
    my_data: MyData, root_user: User, test_tags: list[Tag]
) -> None:
    """Test Tag creation as a ROOT user.

    Creates a tag as a root user.

    Args:
        my_data: a instance of a MyData object.
        root_user: the root user for the context.
        test_tags: a list with tags to add.
    """
    with my_data.get_context(user=root_user) as context:
        context.tags.create(test_tags)

        # Check if they exist
        created_tags = context.tags.retrieve(
            Tag.title.like('test_creation_tag_%')  # type:ignore
        )

        assert len(created_tags) == 3
        assert created_tags[0].title == 'test_creation_tag_1'
        assert created_tags[1].title == 'test_creation_tag_2'
        assert created_tags[2].title == 'test_creation_tag_3'


def test_data_creation_tag_as_normal_user_1(
    my_data: MyData, normal_user_1: User, test_tags: list[Tag]
) -> None:
    """Test User creation as a USER user.

    Creates a tag as a normal user.

    Args:
        my_data: a instance of a MyData object.
        normal_user_1: the first normal user.
        test_tags: a list with tags to add.
    """
    with my_data.get_context(user=normal_user_1) as context:
        context.tags.create(test_tags)

        # Check if they exist
        created_tags = context.tags.retrieve(
            Tag.title.like('test_creation_tag_%')  # type:ignore
        )

        assert len(created_tags) == 3
        assert created_tags[0].title == 'test_creation_tag_1'
        assert created_tags[1].title == 'test_creation_tag_2'
        assert created_tags[2].title == 'test_creation_tag_3'


def test_data_creation_tag_as_normal_user_2(
    my_data: MyData, normal_user_2: User, test_tags: list[Tag]
) -> None:
    """Test User creation as a USER user.

    Creates a tag as a normal user.

    Args:
        my_data: a instance of a MyData object.
        normal_user_2: the first normal user.
        test_tags: a list with tags to add.
    """
    with my_data.get_context(user=normal_user_2) as context:
        context.tags.create(test_tags)

        # Check if they exist
        created_tags = context.tags.retrieve(
            Tag.title.like('test_creation_tag_%')  # type:ignore
        )

        assert len(created_tags) == 3
        assert created_tags[0].title == 'test_creation_tag_1'
        assert created_tags[1].title == 'test_creation_tag_2'
        assert created_tags[2].title == 'test_creation_tag_3'


def test_data_creation_tag_uniqness(
    my_data: MyData, normal_user_1: User
) -> None:
    """Test creating a tags that already exists.

    Should fail since douplicate tags are not allowed.

    Args:
        my_data: a instance of a MyData object.
        normal_user_1: the first normal user.
    """
    with raises(IntegrityError), my_data.get_context(
        user=normal_user_1
    ) as context:
        context.tags.create(Tag(title='normal_user_1_tag_1'))


def test_data_creation_tag_uniqness_non_existing(
    my_data: MyData, normal_user_2: User
) -> None:
    """Test creating a tags that already exists.

    Should not fail since this tag doesnt exist for this user.

    Args:
        my_data: a instance of a MyData object.
        normal_user_2: the scecond normal user.
    """
    with my_data.get_context(user=normal_user_2) as context:
        tag_object = context.tags.create(Tag(title='normal_user_1_tag_1'))

    # Delete the created that
    with my_data.get_context(user=normal_user_2) as context:
        context.tags.delete(tag_object)


def test_data_creation_tag_as_service_account(
    my_data: MyData, service_user: User, test_tags: list[Tag]
) -> None:
    """Test Tag creation as a SERVICE user.

    Creates a tag as a service user. This should fail: service users are not
    allowed to create userspecific resources.

    Args:
        my_data: a instance of a MyData object.
        service_user: the service user.
        test_tags: a list with tags to add.
    """
    with (
        raises(PermissionDeniedError),
        my_data.get_context(user=service_user) as context,
    ):
        context.tags.create(test_tags)


def test_data_creation_tag_as_normal_user_1_wrong_user_id(
    my_data: MyData, normal_user_2: User, test_tags: list[Tag]
) -> None:
    """Test User creation as a USER user.

    Creates a tag as a normal user with a wrong User ID. Should raise an
    PermissionDeniedException exception.

    Args:
        my_data: a instance of a MyData object.
        normal_user_2: the first normal user.
        test_tags: a list with tags to add.
    """
    with (
        my_data.get_context(user=normal_user_2) as context,
        raises(PermissionDeniedError),
    ):
        # Set the wrong user IDs
        for tag in test_tags:
            tag.user_id = 1
        context.tags.create(test_tags)


def test_data_creation_api_clients_as_root(
    my_data: MyData, root_user: User, test_api_clients: list[APIClient]
) -> None:
    """Test API Client creation as a ROOT user.

    Creates a API client as a root user.

    Args:
        my_data: a instance of a MyData object.
        root_user: the root user for the context.
        test_api_clients: a list with API clients to add.
    """
    with my_data.get_context(user=root_user) as context:
        context.api_clients.create(test_api_clients)

        # Check if they exist
        created_api_clients = context.api_clients.retrieve(
            APIClient.app_name.like(  # type: ignore
                'test_creation_api_client_%'
            )
        )

        assert len(created_api_clients) == 3
        assert created_api_clients[0].app_name == 'test_creation_api_client_1'
        assert created_api_clients[1].app_name == 'test_creation_api_client_2'
        assert created_api_clients[2].app_name == 'test_creation_api_client_3'


def test_data_creation_api_clients_as_normal_user_1(
    my_data: MyData, normal_user_1: User, test_api_clients: list[APIClient]
) -> None:
    """Test User creation as a USER user.

    Creates a API client as a normal user.

    Args:
        my_data: a instance of a MyData object.
        normal_user_1: the first normal user.
        test_api_clients: a list with API clients to add.
    """
    with my_data.get_context(user=normal_user_1) as context:
        context.api_clients.create(test_api_clients)

        # Check if they exist
        created_api_clients = context.api_clients.retrieve(
            APIClient.app_name.like(  # type: ignore
                'test_creation_api_client_%'
            )
        )

        assert len(created_api_clients) == 3
        assert created_api_clients[0].app_name == 'test_creation_api_client_1'
        assert created_api_clients[1].app_name == 'test_creation_api_client_2'
        assert created_api_clients[2].app_name == 'test_creation_api_client_3'


def test_data_creation_api_clients_as_normal_user_2(
    my_data: MyData, normal_user_2: User, test_api_clients: list[APIClient]
) -> None:
    """Test API client creation as a USER user.

    Creates a API client as a normal user.

    Args:
        my_data: a instance of a MyData object.
        normal_user_2: the first normal user.
        test_api_clients: a list with API clients to add.
    """
    with my_data.get_context(user=normal_user_2) as context:
        context.api_clients.create(test_api_clients)

        # Check if they exist
        created_api_clients = context.api_clients.retrieve(
            APIClient.app_name.like(  # type: ignore
                'test_creation_api_client_%'
            )
        )

        assert len(created_api_clients) == 3
        assert created_api_clients[0].app_name == 'test_creation_api_client_1'
        assert created_api_clients[1].app_name == 'test_creation_api_client_2'
        assert created_api_clients[2].app_name == 'test_creation_api_client_3'


def test_data_creation_api_clients_as_service_account(
    my_data: MyData, service_user: User, test_api_clients: list[APIClient]
) -> None:
    """Test API client creation as a SERVICE user.

    Creates a API client as a service user. This should fail: service users are
    not allowed to create userspecific resources.

    Args:
        my_data: a instance of a MyData object.
        service_user: the service user.
        test_api_clients: a list with API clients to add.
    """
    with (
        raises(PermissionDeniedError),
        my_data.get_context(user=service_user) as context,
    ):
        context.api_clients.create(test_api_clients)


def test_data_creation_api_clients_as_normal_user_1_wrong_user_id(
    my_data: MyData, normal_user_2: User, test_api_clients: list[APIClient]
) -> None:
    """Test User creation as a USER user.

    Creates a API client as a normal user with a wrong User ID. Should raise an
    PermissionDeniedException exception.

    Args:
        my_data: a instance of a MyData object.
        normal_user_2: the first normal user.
        test_api_clients: a list with API clients to add.
    """
    with (
        my_data.get_context(user=normal_user_2) as context,
        raises(PermissionDeniedError),
    ):
        # Set the wrong user IDs
        for api_client in test_api_clients:
            api_client.user_id = 1
        context.api_clients.create(test_api_clients)


def test_data_creation_api_tokens_as_root(
    my_data: MyData, root_user: User, test_api_tokens: list[APIToken]
) -> None:
    """Test API Token creation as a ROOT user.

    Creates a API Token as a root user.

    Args:
        my_data: a instance of a MyData object.
        root_user: the root user for the context.
        test_api_tokens: a list with API tokens to add.
    """
    with my_data.get_context(user=root_user) as context:
        context.api_tokens.create(test_api_tokens)

        # Check if they exist
        created_api_tokens = context.api_tokens.retrieve(
            APIToken.title.like(  # type: ignore
                'test_creation_api_token_%'
            )
        )

        assert len(created_api_tokens) == 3
        assert created_api_tokens[0].title == 'test_creation_api_token_1'
        assert created_api_tokens[1].title == 'test_creation_api_token_2'
        assert created_api_tokens[2].title == 'test_creation_api_token_3'


def test_data_creation_api_tokens_as_normal_user_1(
    my_data: MyData, normal_user_1: User, test_api_tokens: list[APIToken]
) -> None:
    """Test API token creation as a USER user.

    Creates a API token as a normal user.

    Args:
        my_data: a instance of a MyData object.
        normal_user_1: the first normal user.
        test_api_tokens: a list with API tokens to add.
    """
    with my_data.get_context(user=normal_user_1) as context:
        context.api_tokens.create(test_api_tokens)

        # Check if they exist
        created_api_tokens = context.api_tokens.retrieve(
            APIToken.title.like(  # type: ignore
                'test_creation_api_token_%'
            )
        )

        assert len(created_api_tokens) == 3
        assert created_api_tokens[0].title == 'test_creation_api_token_1'
        assert created_api_tokens[1].title == 'test_creation_api_token_2'
        assert created_api_tokens[2].title == 'test_creation_api_token_3'


def test_data_creation_api_tokens_as_normal_user_2(
    my_data: MyData, normal_user_2: User, test_api_tokens: list[APIToken]
) -> None:
    """Test API token creation as a USER user.

    Creates a API token as a normal user.

    Args:
        my_data: a instance of a MyData object.
        normal_user_2: the first normal user.
        test_api_tokens: a list with API tokens to add.
    """
    with my_data.get_context(user=normal_user_2) as context:
        context.api_tokens.create(test_api_tokens)

        # Check if they exist
        created_api_tokens = context.api_tokens.retrieve(
            APIToken.title.like(  # type: ignore
                'test_creation_api_token_%'
            )
        )

        assert len(created_api_tokens) == 3
        assert created_api_tokens[0].title == 'test_creation_api_token_1'
        assert created_api_tokens[1].title == 'test_creation_api_token_2'
        assert created_api_tokens[2].title == 'test_creation_api_token_3'


def test_data_creation_api_tokens_as_service_account(
    my_data: MyData, service_user: User, test_api_tokens: list[APIToken]
) -> None:
    """Test API tokens creation as a SERVICE user.

    Creates a API tokens as a service user. This should fail: service users are
    not allowed to create userspecific resources.

    Args:
        my_data: a instance of a MyData object.
        service_user: the service user.
        test_api_tokens: a list with API tokens to add.
    """
    with (
        raises(PermissionDeniedError),
        my_data.get_context(user=service_user) as context,
    ):
        context.api_tokens.create(test_api_tokens)


def test_data_creation_api_tokens_as_normal_user_1_wrong_user_id(
    my_data: MyData, normal_user_2: User, test_api_tokens: list[APIToken]
) -> None:
    """Test API token creation as a USER user.

    Creates a API token as a normal user with a wrong User ID. Should raise an
    PermissionDeniedException exception.

    Args:
        my_data: a instance of a MyData object.
        normal_user_2: the first normal user.
        test_api_tokens: a list with API token to add.
    """
    with (
        my_data.get_context(user=normal_user_2) as context,
        raises(PermissionDeniedError),
    ):
        # Set the wrong user IDs
        for api_token in test_api_tokens:
            api_token.user_id = 1
        context.api_tokens.create(test_api_tokens)


def test_data_creation_user_settings_as_root(
    my_data: MyData, root_user: User, test_user_settings: list[UserSetting]
) -> None:
    """Test User Setting creation as a ROOT user.

    Creates a User Setting as a root user.

    Args:
        my_data: a instance of a MyData object.
        root_user: the root user for the context.
        test_user_settings: a list with API tokens to add.
    """
    with my_data.get_context(user=root_user) as context:
        context.user_settings.create(test_user_settings)

        # Check if they exist
        created_user_settings = context.user_settings.retrieve(
            UserSetting.setting.like(  # type: ignore
                'test_creation_user_setting_%'
            )
        )

        assert len(created_user_settings) == 3
        assert (
            created_user_settings[0].setting == 'test_creation_user_setting_1'
        )
        assert (
            created_user_settings[1].setting == 'test_creation_user_setting_2'
        )
        assert (
            created_user_settings[2].setting == 'test_creation_user_setting_3'
        )


def test_data_creation_user_settings_as_normal_user_1(
    my_data: MyData, normal_user_1: User, test_user_settings: list[UserSetting]
) -> None:
    """Test User Setting creation as a USER user.

    Creates a User Setting as a normal user.

    Args:
        my_data: a instance of a MyData object.
        normal_user_1: the first normal user.
        test_user_settings: a list with User Settings to add.
    """
    with my_data.get_context(user=normal_user_1) as context:
        context.user_settings.create(test_user_settings)

        # Check if they exist
        created_user_settings = context.user_settings.retrieve(
            UserSetting.setting.like(  # type: ignore
                'test_creation_user_setting_%'
            )
        )

        assert len(created_user_settings) == 3
        assert (
            created_user_settings[0].setting == 'test_creation_user_setting_1'
        )
        assert (
            created_user_settings[1].setting == 'test_creation_user_setting_2'
        )
        assert (
            created_user_settings[2].setting == 'test_creation_user_setting_3'
        )


def test_data_creation_user_settings_as_normal_user_2(
    my_data: MyData, normal_user_2: User, test_user_settings: list[UserSetting]
) -> None:
    """Test User Setting creation as a USER user.

    Creates a User Setting as a normal user.

    Args:
        my_data: a instance of a MyData object.
        normal_user_2: the first normal user.
        test_user_settings: a list with User Settings to add.
    """
    with my_data.get_context(user=normal_user_2) as context:
        context.user_settings.create(test_user_settings)

        # Check if they exist
        created_user_settings = context.user_settings.retrieve(
            UserSetting.setting.like(  # type: ignore
                'test_creation_user_setting_%'
            )
        )

        assert len(created_user_settings) == 3
        assert (
            created_user_settings[0].setting == 'test_creation_user_setting_1'
        )
        assert (
            created_user_settings[1].setting == 'test_creation_user_setting_2'
        )
        assert (
            created_user_settings[2].setting == 'test_creation_user_setting_3'
        )


def test_data_creation_user_settings_as_normal_user_1_wrong_user_id(
    my_data: MyData, normal_user_2: User, test_user_settings: list[UserSetting]
) -> None:
    """Test User Setting creation as a USER user.

    Creates a User Setting as a normal user with a wrong User ID. Should
    raise an PermissionDeniedException exception.

    Args:
        my_data: a instance of a MyData object.
        normal_user_2: the first normal user.
        test_user_settings: a list with User Settings to add.
    """
    with (
        my_data.get_context(user=normal_user_2) as context,
        raises(PermissionDeniedError),
    ):
        # Set the wrong user IDs
        for user_setting in test_user_settings:
            user_setting.user_id = 1
        context.user_settings.create(test_user_settings)


def test_data_creation_user_settings_as_service_account(
    my_data: MyData, service_user: User, test_user_settings: list[UserSetting]
) -> None:
    """Test User Setting creation as a SERVICE user.

    Creates a USer Setting as a service user. This should fail: service users
    are not allowed to create userspecific resources.

    Args:
        my_data: a instance of a MyData object.
        service_user: the service user.
        test_user_settings: a list with API tokens to add.
    """
    with (
        raises(PermissionDeniedError),
        my_data.get_context(user=service_user) as context,
    ):
        context.user_settings.create(test_user_settings)


def test_data_creation_users_as_normal_user_1_and_aborting_it(
    my_data: MyData, normal_user_1: User
) -> None:
    """Test User creation as a USER user and abort the change.

    Creates a tag as a normal user and avort the change. The created tag should
    no be in the database after the abort.

    Args:
        my_data: a instance of a MyData object.
        normal_user_1: the first normal user.
    """
    with my_data.get_context(user=normal_user_1) as context:
        context.tags.create(Tag(title='test_creation_tag_1_abort'))
        context.abort_session()

    with my_data.get_context(user=normal_user_1) as context:
        # Check if they exist
        created_tags = context.tags.retrieve(
            Tag.title == 'test_creation_tag_1_abort'  # type:ignore
        )

        assert len(created_tags) == 0


def test_data_creation_temporary_token_as_normal_user_2(
    my_data: MyData, normal_user_2: User
) -> None:
    """Test TemporaryToken creation as a USER user.

    Creates a temporary token as a normal user.

    Args:
        my_data: a instance of a MyData object.
        normal_user_2: the first normal user.
    """
    with my_data.get_context(user=normal_user_2) as context:
        temp_token = TemporaryToken(
            token_type=TemporaryTokenType.PASSWORD_RESET
        )
        temp_token.set_random_token()
        token = context.temporary_tokens.create(temp_token)

    with my_data.get_context(user=normal_user_2) as context:
        # Check if they exist
        created_temporary_tokens = context.temporary_tokens.retrieve(
            TemporaryToken.token == token[0].token  # type:ignore
        )

        assert len(created_temporary_tokens) == 1

    # Delete it again
    with my_data.get_context(user=normal_user_2) as context:
        # Check if they exist
        context.temporary_tokens.delete(token)
