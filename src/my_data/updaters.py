"""Module with Updaters.

This module contains the updator classes. These classes are used to update data
in the database. The ResourceManager uses these classes.
"""
from typing import TypeVar

from my_model import MyModel, User, UserRole

from my_data.exceptions import (PermissionDeniedException,
                                WrongDataManipulatorException)

from .data_manipulator import DataManipulator

T = TypeVar('T', bound=MyModel)


class Updater(DataManipulator[T]):
    """Baseclass for Updaters.

    The baseclass for updaters. The sub updaters use this class to make sure
    updaters have the same interface.
    """

    def update(self, models: list[T] | T) -> list[T]:
        """Update data.

        The method to update data in the database.

        Args:
            models: the models to update.

        Returns:
            A list with the updated data models.
        """
        self._logger.debug(
            'User "%s" is updating data for model "%s".',
            self._context_data.user,
            self._database_model)
        return self._add_models_to_session(models)


class UserScopedUpdater(Updater[T]):
    """Updater for UserScoped models.

    This updater should be used for UserScoped models, like Tags and APItokens.
    """

    def update(self, models: list[T] | T) -> list[T]:
        """Update the UserScoped data.

        We override this method from the superclass because we have to make
        sure the `user_id` is set to the correct value first. If this field is
        set to a wrong user_id, we raise an exception.

        Args:
            models: the models to update.

        Returns:
            A list with the created data models.
        """
        models = self._validate_user_scoped_models(models)
        return super().update(models)


class UserUpdater(Updater[T]):
    """Updater for Users.

    This updaters should be used to update Users.
    """

    def update(self, models: list[T] | T) -> list[T]:
        """Update the User data.

        We override this method from the superclass because we have to make
        sure the model is a User model and that the user in the context is
        allowed to update this user. A root user can update ALL users, but a
        normal user can only update his own user.

        Args:
            models: the models to update.

        Raises:
            WrongDataManipulatorException: when the model in the instance is
                not a User.
            PermissionDeniedException: when the model is not the same model as
                set in the instance or when the model has a id set that is
                different then the current user id in the context.

        Returns:
            A list with the created data models.
        """
        if self._database_model is not User:
            raise WrongDataManipulatorException(
                f'The model "{self._database_model}" is not a User')

        # Make sure the `models` are always a list
        models = self._convert_model_to_list(models)

        # Check for all models are a User model and if the `id` field is the
        # same as the current user if this user is a USER user.
        for model in models:
            if not isinstance(model, User):
                raise PermissionDeniedException(  # pragma: no cover
                    f'Expected "{self._database_model}", got "{type(model)}".')

            if self._context_data.user.role == UserRole.USER:
                if model.id != self._context_data.user.id:
                    raise PermissionDeniedException(
                        'User is not allowed to edit this user.')

        return super().update(models)
