"""Module with Creators.

This module contains the creator classes. These classes are used to create data
in the database. The ResourceManager uses these classes.
"""
from typing import TypeVar

from my_model import MyModel, User, UserRole, UserScopedModel

from .data_manipulator import DataManipulator
from .exceptions import (BaseClassCallException, PermissionDeniedException,
                         WrongDataManipulatorException)

T = TypeVar('T', bound=MyModel)


class Creator(DataManipulator[T]):
    """Baseclass for Creators.

    The baseclass for creators. The sub creators use this class to make sure
    creators have the same interface.
    """

    def is_authorized(self) -> bool:
        """Authorize the creation of this data.

        Method that checks if the current context is allowd to create this type
        of model.

        Raises:
            BaseClassCallException: BaseClass method is used.
        """
        raise BaseClassCallException('Method not implemented in baseclass')

    def create(self, models: list[T] | T) -> list[T]:
        """Create data.

        The method to create data in the database.

        Args:
            models: the models to create.

        Raises:
            PermissionDeniedException: when the user is not authorized to
                create this resource.

        Returns:
            A list with the created data models.
        """
        self._logger.debug(
            'User "%s" is creating data for model "%s".',
            self._context_data.user,
            self._database_model)

        if not self.is_authorized():
            raise PermissionDeniedException(
                'Not allowed to create this kind of object within the ' +
                'set context.')
        return self._add_models_to_session(models)


class UserScopedCreator(Creator[T]):
    """Creator for UserScoped models.

    This creator should be used for UserScoped models, like Tags and APItokens.
    """

    def is_authorized(self) -> bool:
        """Check if this user can create tags.

        This method checks if the given databasemodel is, in fact, a UserScoped
        model. If it isn't, it raises a WrongDataManipulatorException. If it
        is, is returns True, indicating that this user can create this type of
        resource.

        Raises:
            WrongDataManipulatorException: when the database_model for this
                instance is not correct.

        Returns:
            True when the user can create these types of objects.
        """
        if not issubclass(self._database_model, UserScopedModel):
            raise WrongDataManipulatorException(
                f'The model "{self._database_model}" is not a UserScopedModel')
        return self._context_data.user.role in (UserRole.ROOT, UserRole.USER)

    def create(self, models: list[T] | T) -> list[T]:
        """Create the UserScoped data.

        We override this method from the superclass because we have to make
        sure the `user_id` is set to the correct value first. If this field is
        already set to a wrong user_id, we raise an exception.

        Args:
            models: the models to create.

        Raises:
            PermissionDeniedException: when the model has a user_id set that is
            different then the current user_id in the context.

        Returns:
            A list with the created data models.
        """
        # Make sure the `models` are always a list
        models = self._convert_model_to_list(models)

        # Add the `user_id` attribute or raise an error when it is already set
        # to a wrong value
        for model in models:
            user_id = getattr(model, 'user_id', None)
            if user_id is not None and user_id != self._context_data.user.id:
                raise PermissionDeniedException(
                    'This user is not allowed to create this resource')
            setattr(model, 'user_id', self._context_data.user.id)

        return super().create(models)


class UserCreator(Creator[T]):
    """Creator for Users.

    This creator should be used to create Users.
    """

    def is_authorized(self) -> bool:
        """Check if this user can create users.

        Checks where the given datamodel is, in fact a User. If it isn't, it
        raises a WrongDataManipulatorException. If it is, it checks the user in
        the context; if there is a user set, it should be a ROOT user. If there
        is no user set, the request is authorized.

        Raises:
            WrongDataManipulatorException: when the database_model for this
                instance is not correct.

        Returns:
            True is this user can create Users and False if this user can't.
        """
        if self._database_model is not User:
            raise WrongDataManipulatorException(
                f'The model "{self._database_model}" is not a UserScopedModel')
        return (not self._context_data.user or
                self._context_data.user.role == UserRole.ROOT)
