"""Module with the `MyDataTableCreator` class.

This class can be used to create the database tables.
"""
import logging

from sqlmodel import SQLModel

from .my_data import MyData


class MyDataTableCreator:
    """Class to create the database tables.

    This class is used to create the database tables. It takes a `MyData`
    object to connect to the database.
    """

    def __init__(self, my_data_object: MyData) -> None:
        """Set the `MyData` object.

        Args:
            my_data_object: the `MyData` object to use to connect to the
                database.
        """
        self._my_data_object = my_data_object
        self._logger = logging.getLogger(f'MyDataTableCreator-{id(self)}')
        self._logger.info('MyDataTableCreator object created')

    def create_db_tables(self, drop_tables: bool = False) -> None:
        """Create the defined models as tables.

        Method to create all tables that are defined in models.

        Args:
            drop_tables: determines if tables should be dropped prior to
                creating them. SQLalchemy will only drop the tables it
                knows about.
        """
        self._my_data_object.create_engine()

        if self._my_data_object.database_engine:
            self._logger.info('Creating tables')
            if drop_tables:
                self._logger.warning('Dropping tables first!')
                SQLModel.metadata.drop_all(
                    self._my_data_object.database_engine)
            SQLModel.metadata.create_all(self._my_data_object.database_engine)
            self._logger.info('Database tables created')
