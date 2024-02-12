"""Module with Retrievers.

This module contains the Retriever classes. These classes are used to retrieve
data from the database. The ResourceManager uses these classes.
"""

from typing import TypeVar

from sqlalchemy.sql.elements import ColumnElement
from sqlalchemy.sql.expression import func
from sqlmodel import select
from sqlmodel.sql.expression import SelectOfScalar

from my_model import MyModel, User, UserRole, UserScopedModel

from .data_manipulator import DataManipulator
from .exceptions import BaseClassCallException, WrongDataManipulatorException

T = TypeVar('T', bound=MyModel)
SelectT = TypeVar('SelectT')


class Retriever(DataManipulator[T]):
    """Baseclass for Retrievers.

    The baseclass for retrievers. The sub retrievers use this class to make
    sure all retrievers have the same interface.
    """

    def get_context_filters(self) -> list[ColumnElement[bool]]:
        """Set default filters for the object.

        Method that returns the default filters for this specific getters. This
        should be used when retrieving resources so only the correct resources
        are retrieved. This method should be overridden by subclasses.

        Raises:
            BaseClassCallException: BaseClass method is used.
        """
        raise BaseClassCallException('Method not implemented in baseclass')

    def _add_filters_to_query(
        self,
        sql_query: SelectOfScalar[SelectT],
        flt: list[ColumnElement[bool]] | ColumnElement[bool] | None = None
    ) -> SelectOfScalar[SelectT]:

        # Filter on the context-based filters
        for filter_item in self.get_context_filters():
            sql_query = sql_query.where(filter_item)

        if isinstance(flt, ColumnElement):
            flt = [flt]

        # Add the filters from the command line
        if flt:
            for filter_item in flt:
                sql_query = sql_query.where(filter_item)

        return sql_query

    def retrieve(
            self,
            flt: list[ColumnElement[bool]] | ColumnElement[bool] | None = None,
            sort: ColumnElement[T] | None = None,
            start: int | None = None,
            max_items: int | None = None) -> list[T]:
        """Retrieve data.

        The method to retrieve data from the database. Can only be done by
        normal users and root users. A Service user, for instance, cannot
        use this method to retrieve data.

        Args:
            flt: a SQLalchemy filter to filter the retrieved data. Can be a
                list of filters, or a single filter.
            sort: the SQLmodel field to sort on.
            start: the index of the first item to retrieve.
            max_items: the maximum number of items to retrieve.

        Returns:
            A list with retrieved data. If no data was found, a empty list is
            returned. If only one item is found, a list with one element is
            returned.
        """
        # Retrieve the resources
        sql_query = select(self._database_model)

        # Add the filters
        sql_query = self._add_filters_to_query(sql_query, flt)

        # Sort the resources
        sql_query = sql_query.order_by(sort)

        # Pagination
        if start is not None and max_items is not None:
            sql_query = sql_query.offset(start).limit(max_items)

        self._logger.debug(
            'User "%s" is retrieving data for model "%s".',
            self._context_data.user,
            self._database_model)

        resources = self._context_data.db_session.exec(sql_query).all()

        # Return the given resources
        return list(resources)

    def count(self,
              flt: list[ColumnElement[bool]] |
              ColumnElement[bool] | None = None) -> int:
        """Retrieve the number of records in the given query.

        Returns the count of records in the given query. This method can be
        used to retrieve the number of records in a query, without retrieving
        the actual records.

        Args:
            flt: a SQLalchemy filter to filter the retrieved data. Can be a
                list of filters, or a single filter.

        Returns:
            The number of records in the given query.
        """
        # Retrieve the resources
        sql_query = select(
            func.count()  # pylint: disable=not-callable
        ).select_from(self._database_model)

        # Add the filters
        sql_query = self._add_filters_to_query(sql_query, flt)

        self._logger.debug(
            'User "%s" is retrieving datacount for model "%s".',
            self._context_data.user,
            self._database_model)

        resources = self._context_data.db_session.exec(sql_query).first()

        # Return the given resources
        return resources if resources else 0


class UserScopedRetriever(Retriever[T]):
    """Retriever for UserScoped models.

    This retriever should be used for UserScoped models, like Tags and
    APITokens.
    """

    def get_context_filters(self) -> list[ColumnElement[bool]]:
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
        return [self._database_model.user_id  # type: ignore
                == self._context_data.user.id]


class UserRetriever(Retriever[T]):
    """Retriever for Users.

    This retrieved should be used for User models.
    """

    def get_context_filters(self) -> list[ColumnElement[bool]]:
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
            return [User.id == self._context_data.user.id]  # type: ignore

        # Root users get no filter
        return []
