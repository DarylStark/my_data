"""TODO: documentation."""

from typing import TypeVar

from sqlalchemy.sql.elements import ColumnElement
from sqlmodel import Session, select

from .data_manipulator import DataManipulator
from .exceptions import BaseClassCallException, WrongDataManipulatorException

from my_model.user_scoped_models import UserRole, User, UserScopedModel

T = TypeVar('T')


class Retriever(DataManipulator):
    """TODO: documentation."""

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
        """TODO: documentation."""

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
    """TODO: documentation."""

    def get_context_filters(self) -> list[ColumnElement]:
        """TODO: documentation."""
        if not issubclass(self._database_model, UserScopedModel):
            raise WrongDataManipulatorException(
                f'The model "{self._database_model}" is not a UserScopedModel')
        return [self._database_model.user_id == self._context_data.user.id]


class UserRetriever(Retriever):
    """TODO: documentation."""

    def get_context_filters(self) -> list[ColumnElement]:
        """TODO: documentation."""
        if self._database_model is not User:
            raise WrongDataManipulatorException(
                f'The model "{self._database_model}" is not a User')
        if self._context_data.user.role == UserRole.USER:
            return [User.id == self._context_data.user.id]

        # Root users get no filter
        return []
