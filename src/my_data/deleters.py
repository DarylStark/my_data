"""Module with Deleters.

This module contains the deleter classes. These classes are used to delete data
from the database. The ResourceManager uses these classes.
"""
from typing import TypeVar

from my_model import MyModel, User, UserRole

from my_data.exceptions import (PermissionDeniedException,
                                WrongDataManipulatorException)

from .data_manipulator import DataManipulator

T = TypeVar('T', bound=MyModel)


class Deleter(DataManipulator[T]):
    """Baseclass for Deleters.

    The baseclass for deleters. The sub deleters use this class to make sure
    deleters have the same interface.
    """

    def delete(self, models: list[T] | T) -> None:
        """Delete data.

        The method to delete data from the database.

        Args:
            models: the models to delete.
        """
        if not isinstance(models, list):
            models = [models]  # pragma: no cover

        self._logger.debug(
            'User "%s" is deleting data for model "%s".',
            self._context_data.user,
            self._database_model)

        # Delete the resources
        for model in models:
            self._context_data.db_session.delete(model)


class UserScopedDeleter(Deleter[T]):
    """Deleter for UserScoped models.

    This deleter should be used for UserScoped models, like Tags and APITokens.
    """

    def delete(self, models: list[T] | T) -> None:
        """Delete the UserScoped data.

        We override this method from the superclass because we have to make
        sure the `user_id` is set to the correct value first. If this field is
        set to a wrong user_id, we raise an exception.

        Args:
            models: the models to delete.
        """
        models = self._validate_user_scoped_models(models)
        super().delete(models)


class UserDeleter(Deleter[T]):
    """Deleter for User models.

    This deleter should be used to delete Users.
    """

    def delete(self, models: list[T] | T) -> None:
        """Delete the User data.

        We override this method from the superclass because we have to make
        sure the model is a User model and that the user in the context is
        allowed to delete this user. A root user can delete ALL users, except
        his own user.

        Args:
            models: the models to delete.

        Raises:
            WrongDataManipulatorException: when the model in the instance is
                not a User.
            PermissionDeniedException: when the model is not the same model as
                set in the instance, when the model is for the current user or
                when the user not allowed to remove this User.
        """
        if self._database_model is not User:
            raise WrongDataManipulatorException(
                f'The model "{self._database_model}" is not a User')

        # Make sure the `models` are always a list
        if not isinstance(models, list):
            models = [models]

        if self._context_data.user.role == UserRole.USER:
            raise PermissionDeniedException(
                'A normal user cannot remove users')

        # Check for all models are a User model and if the `id` field is the
        # same as the current user if this user is a USER user.
        for model in models:
            if not isinstance(model, self._database_model):
                raise PermissionDeniedException(  # pragma: no cover
                    f'Expected "{self._database_model}", got "{type(model)}".')

            if self._context_data.user.id == model.id:
                raise PermissionDeniedException(
                    'Cannot remove the current user.')

        super().delete(models)
