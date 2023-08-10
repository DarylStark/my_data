"""Module with the main class `MyData`.

This module contains the class `MyData`, which is the most important class for
the complete project.
"""

from typing import Any

from my_model.user_scoped_models import (APIClient, APIToken,  # type: ignore
                                         Tag, User, UserRole, UserSetting)
from sqlalchemy.exc import OperationalError
from sqlalchemy.future import Engine
from sqlmodel import Session, SQLModel, and_, create_engine, select

from .context import Context
from .context_data import ContextData
from .exceptions import (DatabaseConnectionException,
                         DatabaseNotConfiguredException,
                         PermissionDeniedException)


class MyData:
    """Main class for the library.

    This class creates the database connection and has a method to expose a
    context.

    Attributes:
        database_engine: the SQLmodel Engine.
        _database_str: the database connection string.
        _database_args: the arguments for the SQLalchemy connection.
    """

    def __init__(self) -> None:
        """Set default values.

        The initiator sets all values to `None`. We can later override these
        values with the `configure` method.
        """
        self.database_engine: Engine | None = None
        self._database_str: str | None = None
        self._database_args: dict[str, Any] | None = None

    def configure(self,
                  db_connection_str: str,
                  database_args: dict[str, Any] | None = None) -> None:
        """Set the database configuration.

        The database configuration is used when the database connection has to
        be made.

        Args:
            db_connection_str: the database connection string for the
                SQLmodel model.
            database_args: a dict with extra configuration for SQLmodel.
        """
        self._database_str = db_connection_str
        self._database_args = database_args

    def create_engine(self, force: bool = False) -> None:
        """Create the database connection.

        Creates the database connection with the given configuration. If the
        configuration is not set, it will raise an exception.

        Args:
            force: if set to True, the database connection will be created even
                if the database connection is already created.

        Raises:
            DatabaseNotConfiguredException: database not configured.
            DatabaseConnectionException: error while connecting to the
                database.
        """
        # Stop if there is already a database engine
        if self.database_engine is not None and not force:
            return

        # Check if the database connection is set
        if self._database_str is None:
            raise DatabaseNotConfiguredException(
                'Database is not configured yet')

        # Connect to the database
        database_args: dict[str, Any] = {
            'url': self._database_str
        }
        if self._database_args:
            database_args.update(self._database_args)

        # Create the database engine
        try:
            self.database_engine = create_engine(**database_args)
        except OperationalError as sa_error:
            raise DatabaseConnectionException(
                'Couldn\'t connect to database') from sa_error

    def create_db_tables(self, drop_tables: bool = False) -> None:
        """Create the defined models as tables.

        Method to create all tables that are defined in models.

        Args:
            drop_tables: determines if tables should be dropped prior to
                creating them. SQLalchemy will only drop the tables it
                knows about.
        """
        self.create_engine()

        if drop_tables:
            SQLModel.metadata.drop_all(self.database_engine)
        SQLModel.metadata.create_all(self.database_engine)

    def get_context(self, user: User) -> Context:
        """Get a Context object for this database.

        Method to create a Context object and return it. The returned Context
        can be used in context manager right away, or as a `normal` object.

        Args:
            user: the user for the context. Is used in the ContextData object
                that is created for the Context object.

        Raises:
            DatabaseNotConfiguredException: method is called before configuring
                the database.

        Returns:
            The created Context object.
        """
        self.create_engine()

        if not self.database_engine:
            raise DatabaseNotConfiguredException(
                'Database is not configured yet')

        return Context(
            database_engine=self.database_engine,
            context_data=ContextData(
                database_engine=self.database_engine,
                user=user)
        )

    def get_context_for_service_user(
            self, username: str, password: str) -> Context:
        """Get a Context object for the database as a service user.

        Method to create a Context object for a service user. The context can
        be used to do the things a service user needs to do, like retrieving
        user objects or API token objects.

        Args:
            username: the username for the service user.
            password: the password for the service user.

        Raises:
            DatabaseNotConfiguredException: method is called before configuring
                the database.
            PermissionDeniedException: when the credentials are incorrect.

        Returns:
            The created Context object.
        """
        self.create_engine()

        if not self.database_engine:
            raise DatabaseNotConfiguredException(
                'Database is not configured yet')

        with Session(self.database_engine) as session:
            sql_query = select(User)
            sql_query = sql_query.where(
                and_(User.username == username,
                     User.role == UserRole.SERVICE))
            users = session.exec(sql_query).all()

            # Check the amount of users we got
            if len(users) != 1:
                raise PermissionDeniedException(
                    f'Service account "{username}" does not exist')

            # Check if the provided credentials are correct
            user = users[0]
            if not user.verify_credentials(username, password):
                raise PermissionDeniedException(
                    f'Password for Service account "{username}" is incorrect')

            return Context(
                database_engine=self.database_engine,
                context_data=ContextData(
                    database_engine=self.database_engine,
                    user=user)
            )

    def create_init_data(self) -> None:
        """Create initializer data.

        Method to create initialization data in the database. Creates data in
        the database that can be used to initialize a database or to create a
        test database. Warning: this method will erase the complete database!
        """
        self.create_db_tables(drop_tables=True)

        with Session(self.database_engine) as session:
            users: list[User] = [
                User(
                    id=1,
                    fullname='root',
                    username='root',
                    email='root@example.com',
                    role=UserRole.ROOT,
                    tags=[
                        Tag(title='root_tag_1'),
                        Tag(title='root_tag_2'),
                        Tag(title='root_tag_3')
                    ],
                    api_clients=[
                        APIClient(
                            app_name='root_api_client_1',
                            app_publisher='root_api_client_1_publisher'),
                        APIClient(
                            app_name='root_api_client_2',
                            app_publisher='root_api_client_2_publisher'),
                        APIClient(
                            app_name='root_api_client_3',
                            app_publisher='root_api_client_3_publisher')
                    ],
                    api_tokens=[
                        APIToken(title='root_api_token_1'),
                        APIToken(title='root_api_token_2'),
                        APIToken(title='root_api_token_3')
                    ],
                    user_settings=[
                        UserSetting(setting='root_test_setting_1',
                                    value='test_value_1'),
                        UserSetting(setting='root_test_setting_2',
                                    value='test_value_2'),
                        UserSetting(setting='root_test_setting_3',
                                    value='test_value_3')
                    ]
                ),
                User(
                    id=2,
                    fullname='Normal user 1',
                    username='normal.user.1',
                    email='normal_user_1@example.com',
                    role=UserRole.USER,
                    tags=[
                        Tag(title='normal_user_1_tag_1'),
                        Tag(title='normal_user_1_tag_2'),
                        Tag(title='normal_user_1_tag_3')
                    ],
                    api_clients=[
                        APIClient(
                            app_name='normal_user_1_api_client_1',
                            app_publisher='normal_user_1_api_client_1_' +
                            'publisher'),
                        APIClient(
                            app_name='normal_user_1_api_client_2',
                            app_publisher='normal_user_1_api_client_2_' +
                            'publisher'),
                        APIClient(
                            app_name='normal_user_1_api_client_3',
                            app_publisher='normal_user_1_api_client_3_' +
                            'publisher')
                    ],
                    api_tokens=[
                        APIToken(title='normal_user_1_api_token_1'),
                        APIToken(title='normal_user_1_api_token_2'),
                        APIToken(title='normal_user_1_api_token_3')
                    ],
                    user_settings=[
                        UserSetting(setting='normal_user_1_test_setting_1',
                                    value='test_value_1'),
                        UserSetting(setting='normal_user_1_test_setting_2',
                                    value='test_value_2'),
                        UserSetting(setting='normal_user_1_test_setting_3',
                                    value='test_value_3')
                    ]
                ),
                User(
                    id=3,
                    fullname='Normal user 2',
                    username='normal.user.2',
                    email='normal_user_2@example.com',
                    role=UserRole.USER,
                    tags=[
                        Tag(title='normal_user_2_tag_1'),
                        Tag(title='normal_user_2_tag_2'),
                        Tag(title='normal_user_2_tag_3')
                    ],
                    api_clients=[
                        APIClient(
                            app_name='normal_user_2_api_client_1',
                            app_publisher='normal_user_2_api_client_1_' +
                            'publisher'),
                        APIClient(
                            app_name='normal_user_2_api_client_2',
                            app_publisher='normal_user_2_api_client_2_' +
                            'publisher'),
                        APIClient(
                            app_name='normal_user_1_api_client_3',
                            app_publisher='normal_user_2_api_client_3_' +
                            'publisher')
                    ],
                    api_tokens=[
                        APIToken(title='normal_user_2_api_token_1',
                                 token='aRlIytpyz61JX2TvczLxJZUsRzk578pE'),
                        APIToken(title='normal_user_2_api_token_2'),
                        APIToken(title='normal_user_2_api_token_3')
                    ],
                    user_settings=[
                        UserSetting(setting='normal_user_2_test_setting_1',
                                    value='test_value_1'),
                        UserSetting(setting='normal_user_2_test_setting_2',
                                    value='test_value_2'),
                        UserSetting(setting='normal_user_2_test_setting_3',
                                    value='test_value_3')
                    ]
                ),
                User(
                    id=4,
                    fullname='Service User - for tests',
                    username='service.user',
                    email='service.user@example.com',
                    role=UserRole.SERVICE,
                )]
            users[0].set_password('root_pw')
            users[1].set_password('normal_user_1_pw')
            users[2].set_password('normal_user_2_pw')
            users[3].set_password('service_password')
            for user in users:
                session.add(user)
            session.commit()
