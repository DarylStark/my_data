"""Module with Updaters.

This module contains the updator classes. These classes are used to update data
in the database. The ResourceManager uses these classes.
"""

from typing import TypeVar

from my_model.user_scoped_models import User, UserScopedModel, UserRole
from sqlmodel import Session

from my_data.exceptions import (PermissionDeniedException,
                                WrongDataManipulatorException)

from .data_manipulator import DataManipulator

T = TypeVar('T')


class Updater(DataManipulator):
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
        # Make sure the `models` are always a list
        if not isinstance(models, list):
            models = [models]

        # Update the resources
        with Session(self._database_engine, expire_on_commit=False) as session:
            for model in models:
                session.add(model)
            session.commit()
        return models


class UserScopedUpdater(Updater):
    """Updater for UserScoped models.

    This updater should be used for UserScoped models, like Tags and APItokens.
    """

    def update(self, models: list[T] | T) -> list[T]:
        """Update the UserScoped data.

        We override this method from the superclass because we have to make 
        sure the `user_id` is set to the correct value first. If this field is
        set to a wrong user_id, we raise an exception.

        Raises:
            WrongDataManipulatorException: when the model in the instance is
                not a UserScopedModel.
            PermissionDeniedException: when the model is not the same model as
                set in the instance or when the model has a user_id set that is
                different then the current user_id in the context.

        Returns:
            A list with the created data models.
        """
        if not issubclass(self._database_model, UserScopedModel):
            raise WrongDataManipulatorException(
                f'The model "{self._database_model}" is not a UserScopedModel')

        # Make sure the `models` are always a list
        if not isinstance(models, list):
            models = [models]

        # Check for all models are a UserScoped model and if the `user_id`
        # field is set to the user_id of the user in the context.
        for model in models:
            if not isinstance(model, self._database_model):
                raise PermissionDeniedException(
                    f'Expected "{self._database_model}", got "{type(model)}".')

            if model.user_id != self._context_data.user.id:
                raise PermissionDeniedException(
                    'This user is not allowed to edit this resource')

        return super().update(models)


class UserUpdater(Updater):
    """Updater for Users.

    This updaters should be used to update Users.
    """

    def update(self, models: list[T] | T) -> list[T]:
        """Update the User data/

        We override this method from the superclass because we have to make
        sure the model is a User model and that the user in the context is
        allowed to update this user. A root user can update ALL users, but a
        normal user can only update his own user.
        """
        if self._database_model is not User:
            raise WrongDataManipulatorException(
                f'The model "{self._database_model}" is not a User')

        # Make sure the `models` are always a list
        if not isinstance(models, list):
            models = [models]

        # Check for all models are a User model and if the `id` field is the
        # same as the current user if this user is a USER user.
        for model in models:
            if not isinstance(model, self._database_model):
                raise PermissionDeniedException(
                    f'Expected "{self._database_model}", got "{type(model)}".')

            if self._context_data.user.role == UserRole.USER:
                if model.id != self._context_data.user.id:
                    raise PermissionDeniedException(
                        'User is not allowed to edit this user.')

        return super().update(models)
