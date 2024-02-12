"""Module with the `ContextData` class.

This module contains the `ContextData` class that can be used to specify the
context-variables in which a `Context` object should operate.
"""
from sqlalchemy.future import Engine
from sqlmodel import Session

from my_model import User


class ContextData:
    """Class with ContextData.

    Dataclass that contains the data for a `Context`-object. The properties
    defined in this class define the context that is being used.

    Attributes:
        user: a user object representing this context.
        db_session: a SQLalchemy session that can be used.
    """

    def __init__(self, database_engine: Engine, user: User) -> None:
        """Create the ContextData object.

        The initiator sets the values for the ContextData and creates a
        SQLalchmey Session.

        Args:
            database_engine: a SQLalchemy Engine to bind the Session to.
            user: a User to bind the Context to
        """
        self.user: User = user
        self.db_session = Session(database_engine, expire_on_commit=False)

    def commit_session(self) -> None:
        """Commit the database session.

        Method to commit the changes in the session. This should be done when
        the Context is ready with this ContextData object.
        """
        if self.db_session:
            self.db_session.commit()

    def close_session(self) -> None:
        """Commit and closes the database sessions.

        Method to cclose the session. This should be done when the Context is
        ready with this ContextData object.
        """
        if self.db_session:
            self.db_session.close()

    def abort_session(self) -> None:
        """Abort the database session.

        Method to abort the changes in the session. This is not done
        automatically and should be invoked by the user when he made changes
        that should be aborted before commited. After the abort, the session
        is _not_ closed; the user has to do that himself.
        """
        if self.db_session:
            self.db_session.rollback()
