"""Module with Retrievers.

This module contains the Retriever classes. These classes are used to retrieve
data from the database. The ResourceManager uses these classes.
"""

from typing import TypeVar

from sqlalchemy.sql.elements import ColumnElement
from sqlmodel import Session, select

from .data_manipulator import DataManipulator
from .exceptions import BaseClassCallException, WrongDataManipulatorException

from my_model.user_scoped_models import UserRole, User, UserScopedModel

T = TypeVar('T')


class Retriever(DataManipulator):
    """Baseclass for Retrievers.

    The baseclass for retrievers. The sub retrievers use this class to make
    sure all retrievers have the same interface.
    """

    def get_context_filters(self) -> list[ColumnElement]:
        """Default filters for the object.

        Method that returns the default filters for this specific getters. This
        should be used when retrieving resources so only the correct resources
        are retrieved. This method should be overridden by subclasses.

        Raises:
            BaseClassCallException: BaseClass method is used.
        """
        raise BaseClassCallException('Method not implemented in baseclass')

    def retrieve(
            self,
            flt: list[ColumnElement] | ColumnElement | None = None) -> list[T]:
        """Retrieve data.

        The method to retrieve data from the database.

        Args:
            flt: a SQLalchemy filter to filter the retrieved data. Can be a
                list of filters, or a single filter.

        Returns:
            A list with retrieved data. If no data was found, a empty list is
            returned. If only one item is found, a list with one element is
            returned.
        """

        # Retrieve the resources
        with Session(self._database_engine) as session:
            sql_query = select(self._database_model)

            # Filter on the context-based filters
            for filter_item in self.get_context_filters():
                sql_query = sql_query.where(filter_item)

            if isinstance(flt, ColumnElement):
                flt = [flt]

            # Add the filters from the command line
            if flt:
                for filter_item in flt:
                    sql_query = sql_query.where(filter_item)

            resources = session.exec(sql_query).all()

        # Return the given resources
        return resources


class UserScopedRetriever(Retriever):
    """Retriever for UserScoped models.

    This retriever should be used for UserScoped models, like Tags, APITokens
    and Users itself.
    """

    def get_context_filters(self) -> list[ColumnElement]:
        """Get default filters for the current context.

        Returns the fitlers that are relevant for the current context. In the
        case of UserScoped models, this method will return filters to make sure
        only the data for the user in the context are returned.

        If the model is not a UserScoped model, the method will raise an
        exception.

        Raises:
            WrongDataManipulatorException: when the model for the class is not
                a UserScoped model.

        Returns:
            A list with the SQLalchmey filters.
        """
        if not issubclass(self._database_model, UserScopedModel):
            raise WrongDataManipulatorException(
                f'The model "{self._database_model}" is not a UserScopedModel')
        return [self._database_model.user_id == self._context_data.user.id]


class UserRetriever(Retriever):
    """Retriever for Users.

    This retrieved should be used for USer models.
    """

    def get_context_filters(self) -> list[ColumnElement]:
        """Get default filters for the current context.

        Returns the fitlers that are relevant for the current context. In this
        case, it returns no filters is the user is a ROOT user, since that user
        is allowed to see all users. If the user is a normal user, it returns
        a filter that will make sure only the own user will be selected.

        If the model is not a User model, the method will raise an exception.

        Raises:
            WrongDataManipulatorException: when the model for the class is not
                a User model.

        Returns:
            A list with the SQLalchmey filters.
        """
        if self._database_model is not User:
            raise WrongDataManipulatorException(
                f'The model "{self._database_model}" is not a User')
        if self._context_data.user.role == UserRole.USER:
            return [User.id == self._context_data.user.id]

        # Root users get no filter
        return []