Setup database connection
=========================

The main class for the library is the ``MyData`` class. This class should be initiated to use the ``my-data`` package and all related functionality. After initializing it, you can configure it to use a specific datbase string and optionally arguments that you would like to give to this database connection. You use the ``configure`` method to do so.

**Example:**

.. code-block:: python

    from my_data import MyData

    my_data = MyData()
    my_data.configure(
        db_connection_str='sqlite:////home/user/my-data.db',
        database_args={
            'echo': True
        },
        service_user='service.user',
        service_password='service.pass'
    )

This will create a ``MyData`` object that uses a local SQLite database file located at ``/home/user/my-data.db``. The database will be configured to echo all SQL commands to the console. It also sets the Service User and Service Password for the tasks related to service users. These credentials are not checked now; they are checked when the service user is used.

Creating tables
---------------

After you configured the object, you can optionally create the tables. This is usefull when creating a new database. To create the needed tables, you can use the ``create_db_tables``` method of the ``MyDataTableCreator`` class. The first and only argument of this method specifies if existing tables should be dropped and recreated. By default, this is set to ``False``.

.. warning::

    If you specify to drop the tables, you can have data loss! Be aware when doing this with production databases! There are no rollback mechanisms built into the ``my-data`` package!

To create the tables, you use the following code:

.. code-block:: python
    
    my_data_creator = MyDataTableCreator(my_data_object=my_data)
    my_data_creator.create_db_tables(drop_tables=False)

Creating initialization data
----------------------------

After you have a database with the correct schema, you can optionally create initialization data. This can be used for testing or when creating a initial database. To do this you need a JSON file with the data that needs to be created.

**Example JSON file:**

.. code-block:: json

    {
        "api_scopes": [
            {
                "id": 1,
                "module": "users",
                "subject": "create"
            },
            {
                "id": 2,
                "module": "users",
                "subject": "retrieve"
            }
        ],
        "users": [
            {
                "id": 1,
                "fullname": "root",
                "username": "root",
                "email": "root@example.com",
                "role": 1,
                "_password": "root_pw",
                "_tags": [
                    {
                        "title": "root_tag_1"
                    }
                ],
                "_api_clients": [
                    {
                        "id": 100,
                        "app_name": "root_api_client_1",
                        "app_publisher": "root_api_client_1_publisher"
                    }
                ],
                "_api_tokens": [
                    {
                        "id": 100
                        "title": "root_api_token_1",
                        "token": "MHxHL4HrmmJHbAR1b0gV4OkpuEsxxmRL",
                        "enabled": false,
                        "api_client_id": 100
                    }
                ],
                "_user_settings": [
                    {
                        "setting": "root_test_setting_1",
                        "value": "test_value_1"
                    }
                ]
            },
            {
                "id": 1,
                "fullname": "Service User - for tests",
                "username": "service.user",
                "email": "service.user@example.com",
                "role": 2,
                "_password": "service_password"
            }
        ],
        "api_token_scopes": [
            {
                "api_token_id": 100,
                "api_scope_id": 1
            }
        ]
    }

To import this JSON file, save it as ``test_data.json`` and import it with the following Python code:

.. code-block:: python

    from my_data.data_loader import DataLoader, JSONDataSource

    loader = DataLoader(
        my_data_object=my_data,
        data_source=JSONDataSource(
            './tests/test_data.json'))
    loader.load()

If you want to import something else then a JSON file, you can write your own data source class and use it with the ``DataLoader`` class. To do this, create a class and subclass it from the ``DataSource`` class. This class should have a ``load`` method that returns a dictionary with the data that needs to be imported.