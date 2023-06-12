"""The creators for the ResourceManager.

This module contains the Creators for the ResourceManager. It contains the
base-class and the subclasses.
"""
from my_model._model import Model  # type: ignore
from my_model.user import User, UserRole  # type: ignore
from sqlmodel import SQLModel

from .crud_base import CRUDBase
from .db_connection import db_connection
from .db_models import DBUser
from .exceptions import PermissionDeniedException, WrongModelException


class Creator(CRUDBase):
    """Base Creator class.

    The base Creator class should be used as the base class for specific
    Creator-classes. The base class defines the interface for all
    Creator-classes.
    """

    def get_updated_model(self, data: Model) -> SQLModel:
        """Convert the `my-model` model to a DB model and set needed values.

        Returns a DB model of the given `my-model` Model with the correct
        value set. It can, for instance, set the `user_id` for resources that
        are specific to users.

        Args:
            data: the `my-model` instance.

        Raises:
            NotImplementedError: raised when this method is used for the base
                class instead of a subclass.
        """
        raise NotImplementedError(
            'Method `get-updated-model` is not implemented for this type')

    def create(self, models: Model | list[Model]) -> None:
        """Create the data.

        Converts the `data` in `my-model` into a DB Models and adds them to the
        database.

        Args:
            models: the `my-model` instances. Can be one, or a list of multiple
                resources.

        Raises:
            WrongModelException: when the given model is not the same as the
                set model in the object.
        """
        # Make sure the data is a list. We need this later in the list
        # comprehension.
        if not isinstance(models, list):
            models = [models]

        # Check if they are all of the correct type. We could this with a smart
        # list comprehension to create a list of boolean values from
        # `isinstance` and then use `all()` to check if they are all of the
        # correct type, but that would be inefficient with bigger lists.
        # Instead, we loop over them and stop as soon as we find one that isn't
        # the correct model.
        for model in models:
            if not isinstance(model, self._model):
                raise WrongModelException(
                    f'Expected model "{self._model}", not "{type(model)}"')

        # Convert all Models to DBModels.
        db_models = [self.get_updated_model(model) for model in models]

        with db_connection.get_session() as session:
            # Add the resource to the DB
            for model in db_models:
                session.add(model)
            session.commit()


class UserSpecificCreator(Creator):
    """Creator for user specific resources.

    This creator should be used for resources that are bound to specific users,
    like tags and API tokens.
    """

    def get_updated_model(self, data: Model) -> SQLModel:
        """Convert the `my-model` model to a DB model and set the user id.

        Returns a DB model of the given `my-model` mddel with the correct
        `user_id` set. If the user-object in the context is not set, we raise
        a exception.

        Args:
            data: the `my-model` instance.

        Returns:
            SQLModel: the generated DB model with the `user_id` set.

        Raises:
            PermissionDeniedException: when no user is set in the context data.
        """
        if not self._context_data or not self._context_data.user:
            raise PermissionDeniedException('No user set in the resource.')

        # Create the DB object
        db_object = self._db_model(**data.dict())

        # Set the user_id
        db_object.user_id = self._context_data.user.id

        # Return the DB object
        return db_object


class UserCreator(Creator):
    """Creator for user specific resources.

    This creator should be used to create users.
    """

    def get_updated_model(self, data: User) -> DBUser:
        """Convert the User model to a DBUser.

        Returns a DBModel instance created from the given User instance. If the
        user-object in the context is not set, we raise an exception. If the
        user-object is set but not a root user, we also raise a exception. Only
        root users are allowed to create users.

        Args:
            data: the `User` instance.

        Returns:
            DBUser: the generated DBUser.

        Raises:
            PermissionDeniedException: when no user is set in the context data,
                or when a normal user tries to create a user.
        """
        if not self._context_data or not self._context_data.user:
            raise PermissionDeniedException('No user set in the resource.')
        if self._context_data.user.role != UserRole.ROOT:
            raise PermissionDeniedException('No permissions to create users.')

        # Return the DB object
        return DBUser(**data.dict())
