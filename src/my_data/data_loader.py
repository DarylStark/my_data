"""Module with the DataLoader class and specific Data Sources."""
import json
import logging
from abc import ABC, abstractmethod
from typing import Type

from sqlmodel import Session, SQLModel

from my_data.my_data import MyData
from my_model import (APIClient, APIScope, APIToken, APITokenScope, MyModel,
                      Tag, User, UserSetting)


class DataSource(ABC):
    """Abstract class for a data loader source."""

    @abstractmethod
    def load(self) -> list[SQLModel]:
        """Load the data from the source and return a list with loaded data.

        Returns:
            A list with loaded data.
        """


class JSONDataSource(DataSource):
    """Data source for JSON files."""

    def __init__(self, json_filename: str) -> None:
        """Initialize the JSONDataSource object.

        Args:
            json_filename: the filename of the JSON file to load.
        """
        self._json_filename = json_filename

    def load(self) -> list[SQLModel]:
        """Load the data from a JSON file and return a list with loaded data.

        Returns:
            A list with loaded data.
        """
        resources_to_add: list[SQLModel] = []

        # Dict with userscoped resources as found in the JSON file.
        user_scoped_resources: dict[str, Type[MyModel]] = {
            '_tags': Tag,
            '_api_clients': APIClient,
            '_api_tokens': APIToken,
            '_user_settings': UserSetting
        }

        # Load the JSON data
        with open(self._json_filename, 'r', encoding='utf-8') as json_file:
            json_data = json.load(json_file)

        # Create the objects for API scopes
        for api_scope in json_data['api_scopes']:
            # Create the API scope object
            api_scope_object = APIScope(**api_scope)
            resources_to_add.append(api_scope_object)

        # Create the objects for users
        for user in json_data['users']:
            # Extract the fields that are User specific
            user_specific_fields = {
                key: value for key, value in user.items() if key[0] != '_'
            }

            # Create the user object
            user_object = User(**user_specific_fields)

            # Get the password
            if user.get('_password'):
                user_object.set_password(user['_password'])

            # Add connected resources

            # Add the tags
            for field, object_type in user_scoped_resources.items():
                if user.get(field):
                    setattr(user_object, field[1:], [
                        object_type(**tag) for tag in user[field]
                    ])

            # Add it to the list
            resources_to_add.append(user_object)

        # Create the objects for APITokenScopes
        for api_token_scope in json_data['api_token_scopes']:
            # Create the API scope object
            api_token_scope_object = APITokenScope(**api_token_scope)
            resources_to_add.append(api_token_scope_object)

        return resources_to_add


class DataLoader:
    """Class to load data in the database.

    Uses a configured DataLoaderSource object to load the data. By using this,
    the DataLoader object can be used to load data from different sources.
    """

    def __init__(
            self,
            my_data_object: MyData,
            data_source: DataSource) -> None:
        """Initialize the DataLoader object.

        Sets the MyData object and the DataLoaderSource object to use to load
        data.

        Args:
            my_data_object: the MyData object.
            data_source: the DataSource object to use to load data.
        """
        self._logger = logging.getLogger(f'DataLoader-{id(self)}')
        self._logger.info('DataLoader object created')
        self._my_data_object = my_data_object
        self._data_loader = data_source

    def load(self) -> None:
        """Load the data in the database."""
        self._logger.debug('Retrieving data')
        data = self._data_loader.load()
        self._logger.debug('Items to load: %s', len(data))
        with Session(self._my_data_object.database_engine) as session:
            session.add_all(data)
            session.commit()
