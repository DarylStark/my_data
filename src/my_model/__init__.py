"""My Model Package.

This package contains the data model for the complete My application. It
specifies the models that should be used by other packages to create,
retrieve and update items.

The models in this package use the SQLModel class as baseclass so that the
complete validation of Pydantic can be used, and the ORM database structure
of SQLalchemy can be used, without having to use two seperate data schemas.
"""

from .model import (
    APIClient,
    APIScope,
    APIToken,
    APITokenScope,
    MyModel,
    Tag,
    TokenModel,
    User,
    UserRole,
    UserScopedModel,
    UserSetting,
)

__version__ = '1.2.3-dev'

__all__ = [
    'MyModel',
    'UserRole',
    'User',
    'APITokenScope',
    'APIScope',
    'UserScopedModel',
    'TokenModel',
    'APIClient',
    'APIToken',
    'Tag',
    'UserSetting',
]
