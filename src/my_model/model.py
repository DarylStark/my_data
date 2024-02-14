"""Module that contains the classes for all models.

This module contains the classes for models that are specific for a user, like
the User model itself and models that are created within the user namespace.
Examples for these models are API Tokens and Tags. To make sure we don't have
any code duplication, we use specific base classes: UserScopedModel for models
that are namespaced within a User and TokenModel for models that contain a
token of some sort.

There are also some classes that are used to link models together, like
APITokenScope, which is used to link API Tokens to API Scopes. To get this
working, we have to define the APIScope model in this module too.
"""

import random
import string
from datetime import datetime
from enum import Enum

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from pydantic import validate_call
from pyotp import TOTP, random_base32
from sqlmodel import Field, Relationship, SQLModel
from sqlmodel._compat import SQLModelConfig


class MyModel(SQLModel):
    """SQLmodel basemodel for all models.

    Should be used for all models. This base class defines the Pydantic
    configuration that all models should use. Because we use SQLmodel, these
    models are usable for generic modeling _and_ for SQLalchemy ORM.

    Attributes:
        id: the unique ID for this object. If this object is used for a SQL
            database, it is the primary key.
    """

    id: int | None = Field(default=None, primary_key=True)
    model_config = SQLModelConfig(validate_assignment=True)

    # The `__pydantic_extra__` attribute is set to None, just to make sure the
    # library can find this attribute. It may be unneeded in future versions of
    # SQLmodel, but right now, in version `0.0.14`, is is needed or it will
    # trigger a error.
    __pydantic_extra__ = None

    @validate_call
    def get_random_string(self,
                          min_length: int,
                          max_length: int,
                          include_punctation: bool = True) -> str:
        """
        Return a random generated string.

        Can be used to generate a random string for tokens, passwords or other
        secrets. The min_length and max_length arguments can be used to set the
        size limits for the random string. The method will create a string of
        random length within these limits. If you need a specific length, make
        sure that both min_length and max_length are of equal val23
        ue.

        Args:
            min_length: the minimum length of the generated random string
            max_length: the maximum length of the generated random string
            include_punctation: defines if punctation should be used

        Returns:
            A string with the randomly generated characters.
        """
        # Create the characterset
        characters = string.ascii_letters
        characters += string.digits

        if include_punctation:
            characters += string.punctuation

        # Create the random character string
        length = random.randint(min_length, max_length)
        random_token_chars = [random.choice(characters)
                              for i in range(0, length)]
        random_string = ''.join(random_token_chars)

        # Return the created string
        return random_string


class UserRole(Enum):
    """The roles a user can have.

    Attributes:
        ROOT: for root users; users with god-mode permissions.
        SERVICE: for service accounts.
        USER: normal users
    """

    ROOT = 1
    SERVICE = 2
    USER = 3


class User(MyModel, table=True):
    """Model for Users.

    The user model is meant for local useraccounts.

    Attributes:
        created: the datetime when this user was created
        fullname: the fullname for the user
        username: the username for the user
        email: the emailaddress of the user
        role: the role of the user (see UserRole)
        password_hash: the hashed password of the user
        password_date: the date when the password was set
        second_factor: either a random base32 that indicates a secret for the
            second factor of the user, or None if no secret is set.
        api_clients: a list of API clients for this user.
        api_tokens: a list of API tokens for this user.
        tags: a list of tags for this user.
        user_settings: a list of settings for this user.
    """

    created: datetime = Field(default_factory=datetime.utcnow)
    fullname: str = Field(schema_extra={'pattern': r'^[A-Za-z0-9\- ]+$'},
                          max_length=128)
    username: str = Field(
        schema_extra={'pattern': r'^[a-zA-Z][a-zA-Z0-9_\.]+$'},
        max_length=128,
        unique=True)
    email: str = Field(
        schema_extra={
            'pattern': r'^[a-z0-9_\-\.]+\@[a-z0-9_\-\.]+\.[a-z\.]+$'},
        max_length=128,
        unique=True)
    role: UserRole = Field(default=UserRole.USER)
    password_hash: str | None = None
    password_date: datetime = Field(default_factory=datetime.utcnow)
    second_factor: None | str = Field(
        default=None,
        schema_extra={'pattern': r'^[A-Z0-9]+$'}, max_length=64,
        unique=True)

    # Relationships
    api_clients: list['APIClient'] = Relationship(back_populates='user')
    api_tokens: list['APIToken'] = Relationship(back_populates='user')
    tags: list['Tag'] = Relationship(back_populates='user')
    user_settings: list['UserSetting'] = Relationship(back_populates='user')

    @validate_call
    def set_password(self, password: str) -> None:
        """Set the password for the user.

        Args:
            password: the password for the user.
        """
        hasher = PasswordHasher()
        self.password_hash = hasher.hash(password)
        self.password_date = datetime.utcnow()

    @validate_call
    def set_random_second_factor(self) -> str:
        """Set a random second factor secret for the user.

        Returns:
            The generated second factor secret.
        """
        self.second_factor = random_base32()
        return self.second_factor

    @validate_call
    def disable_second_factor(self) -> None:
        """Disable the second factor for the user."""
        self.second_factor = None

    @validate_call
    def verify_credentials(self,
                           username: str,
                           password: str,
                           second_factor: str | None = None) -> bool:
        """Verify the credentials for a user.

        Args:
            username: the username to verify
            password: the password to verify
            second_factor: the second factor for the user, or None if this
                doesn't need to be validated.

        Returns:
            True if the credentials where corret for this useraccount. False if
            these credentials where not correct.
        """
        hasher = PasswordHasher()
        try:
            if self.password_hash:
                credentials = (username == self.username and
                               hasher.verify(self.password_hash, password))
            else:
                raise VerifyMismatchError
        except VerifyMismatchError:
            return False

        if self.second_factor:
            return (credentials and
                    second_factor == TOTP(self.second_factor).now())

        return credentials


class APITokenScope(SQLModel, table=True):
    """Link table to connect API tokens to API scopes.

    Attributes:
        api_token_id: the ID for the API token.
        api_scope_id: the ID for the API scope.
    """

    api_token_id: int = Field(
        default=None, foreign_key='apitoken.id', primary_key=True)
    api_scope_id: str = Field(
        default=None, foreign_key="apiscope.id", primary_key=True)


class APIScope(MyModel, table=True):
    """Model for API scopes.

    Attributes:
        module: the module for the API scope.
        subject: the subject for the API scope.
    """

    module: str = Field(max_length=32)
    subject: str = Field(max_length=32)

    # Relationships
    api_tokens: list['APIToken'] = Relationship(
        back_populates='token_scopes',
        link_model=APITokenScope)

    @property
    def full_scope_name(self) -> str:
        """Property for the full scope name.

        Returns the complete scope name for this scope.

        Returns:
            The full scope name as string.
        """
        return f'{self.module}.{self.subject}'


class UserScopedModel(MyModel):
    """Basemodel for models that are user scoped.

    Defines the `user_id` attribute for models that are scoped to a specific
    user. By putting this in a seperate base class, we can prevent duplicate
    code.

    Attributes:
        user_id: the unique ID for a user.
    """

    user_id: int | None = Field(default=None, foreign_key='user.id')


class TokenModel(UserScopedModel):
    """Basemodel for classes that use tokens.

    Defines the `set_random_token` method that can and should be used to
    generate a random token.

    Attributes:
        token: the token for the object
    """

    token: str | None = Field(
        default=None,
        min_length=32,
        max_length=32,
        schema_extra={'pattern': r'^[a-zA-Z0-9]{32}$'},
        unique=True
    )

    @validate_call
    def set_random_token(self, force: bool = False) -> str:
        """Set a random generated token.

        Args:
            force: if set to True, the token will be generated even if None is
                set. If set to False, a token will only be set if there is no
                token already set.

        Returns:
            A string with the token that is set.

        Raises:
            PermissionError: a token was already set and `force` was not set to
            True.
        """
        if self.token is None or force:
            # Generate random token
            self.token = self.get_random_string(
                min_length=32,
                max_length=32,
                include_punctation=False)

            return self.token

        # Token was already set but force wasn't; raise an error
        raise PermissionError('Token is already set')


class APIClient(TokenModel, table=True):
    """Model for API clients.

    Attributes:
        created: the datetime when this client was created.
        expires: the datetime when this client will expire.
        enabled: defines it the client is enabled.
        app_name: the name for the app.
        app_publisher: the name for the publisher of the app.
        redirect_url: a URL where the user will be redirected after a token has
            been granted. Can and should be used by web applications.
        user: the user object for the owner.
    """

    created: datetime = Field(default_factory=datetime.utcnow)
    expires: datetime = Field(default_factory=datetime.utcnow)
    enabled: bool = True
    app_name: str = Field(max_length=64)
    app_publisher: str = Field(max_length=64)
    redirect_url: str | None = Field(
        default=None,
        schema_extra={'pattern': r'^https?://'},
        max_length=1024)

    # Relationships
    user: User = Relationship(back_populates='api_clients')
    api_tokens: list['APIToken'] = Relationship(back_populates='api_client')


class APIToken(TokenModel, table=True):
    """Model for API clients.

    Attributes:
        created: the datetime when this token was created.
        expires: the datetime when this token will expire.
        api_client_id: the API Client for this token. This field is optional
            because
        enabled: defines it the token is enabled.
        title: the title for the token.
        user: the user object for the owner.
    """

    created: datetime = Field(default_factory=datetime.utcnow)
    expires: datetime = Field(default_factory=datetime.utcnow)
    api_client_id: int | None = Field(default=None, foreign_key='apiclient.id')
    enabled: bool = True
    title: str = Field(max_length=64)

    # Relationships
    user: User = Relationship(back_populates='api_tokens')
    api_client: APIClient = Relationship(back_populates='api_tokens')
    token_scopes: list[APIScope] = Relationship(
        back_populates='api_tokens',
        link_model=APITokenScope)


class Tag(UserScopedModel, table=True):
    """Model for Tags.

    The tag model is meant to represent a tag. A tag can be given to a
    multitude of resources in the application, like days, notes, RSS feeds,
    etc. They are meant to group everything together that needs to be together.

    Attributes:
        title: the name of the tag.
        color: a specific color for the tag. This color can be used by
            view-services to display the tag in a distinguishable way. The
            color should be represented as a 6-character hex string (RGB).
        user: the user object for the owner.
    """

    title: str = Field(max_length=128)
    color: str | None = Field(
        default=None, schema_extra={'pattern': r'^[a-fA-F0-9]{6}$'},
        min_length=6, max_length=6)

    # Relationships
    user: User = Relationship(back_populates='tags')


class UserSetting(UserScopedModel, table=True):
    """Model for User Settings.

    The User Settings model should be used by services that use this model to
    set specific settings, like themes, notification settings or other user
    specific settings. Should be used as a key/value store.

    Attributes:
        setting: the name of the setting.
        value: the value for the setting.
        user: the user object for the owner.
    """

    setting: str = Field(max_length=32)
    value: str = Field(max_length=32)

    # Relationships
    user: User = Relationship(back_populates='user_settings')
