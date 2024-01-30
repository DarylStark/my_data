Setup database connection
=========================

After creating a object of ``MyData``, you can configure it with a database string that tells the object how to connect to the database. The connection string is a SQLalchmey database connection string. More information about this can be found in the `SQLalchmey documentation <https://docs.sqlalchemy.org/en/20/core/engines.html#database-urls>`_. Besides the database connection string, you can optionally give ``database_args`` to configure the database to your needs.

To configure the ``MyData`` object, use the following code:

.. code-block:: python

    from my_data.my_data import MyData

    data_object = MyData()
    data_object.configure(
        db_connection_str='sqlite:///:memory:',
        database_args={
            'echo': True
        }
    )

After you configured the database, you can instruct the ``MyData``  to create a engine with the ``create_engine()`` method. This creates the SQLalchmey Database Engine. If you don't do this, this is done automatically when executing a method that needs a Database Engine.

Creating tables
---------------

After you configured the object, you can optionally create the tables and initialization data. To creathe the needed tables, you can use the ``create_db_tables``` method. The first and only argument of this method specifies if existing tables should be dropped and recreated. By default, this is set to ``False``.

.. warning::

    If you specify to drop the tables, you can have data loss! Be aware when doing this with production databases! There are no rollback mechanisms built into the ``my-data`` package!

To create the tables, you use the following code:

.. code-block:: python

    my_data.create_db_tables(drop_tables=False)

Creating initialization data
----------------------------

After you have a database with the correct schema, you can optionally create initialization data. This can be used for testing or when creating a initial database.

.. code-block:: python

    from my_data.data_loader import DataLoader, JSONDataSource

    loader = DataLoader(
        my_data_object=my_data,
        data_source=JSONDataSource(
            './tests/test_data.json'))
    loader.load()

