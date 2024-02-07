Database string examples
========================

To use the ``MyData`` class, you have to configure it with a database string. The database string is a string that contains all the information needed to connect to a database. This page gives a few examples of database strings that you can use to connect to your database. The ``MyData`` class uses ``SQLmodel`` to connect to the database, so the database string is the same as the one used by ``SQLmodel``.

This page describes three types of database strings:

- SQLite
- MySQL
- PostgreSQL

SQLite
------

SQLite is a serverless database, which means that it doesn't require a separate server process. The database is stored in a single file on disk. To connect to a SQLite database, you can use a database string like this:

.. code-block::
    
    sqlite:///<filename>

The filename is the path to the SQLite database file. If the file doesn't exist, it will be created. If the file does exist, it will be opened. Here's an example of a database string that connects to a SQLite database file named ``mydatabase.db`` in the current directory:

.. code-block::
    
    sqlite:///mydatabase.db

And here's an example of a database string that connects to a SQLite database file named ``mydatabase.db`` in a directory named ``app`` in the root of the filesystem:

.. code-block::
    
    sqlite:////app/mydatabase.db

You can also use in in-memory database by using the special filename ``:memory:``. This type of database is very usefull for unit testing.

.. code-block::
    
    sqlite:///:memory:

.. warning::

    An in-memory database is deleted as soon as the connection to it is closed, so you can't use it to persist data between different runs of your application.

MySQL
-----

To connect to a MySQL database, you can use a database string like this:

.. code-block::
    
    mysql[+driver]://<username>:<password>@<hostname>/<dbname>

Here's an example of a database string that connects to a MySQL database named ``mydatabase`` on a server named ``myserver`` with the username ``myusername`` and the password ``mypassword``. It uses the default MySQL driver:

.. code-block::
    
    mysql://myusername:mypassword@myserver/mydatabase

If you want to create the connection using the ``pymysql``, you can use the following database string:

.. code-block::
    
    mysql+pymysql://myusername:mypassword@myserver/mydatabase

.. important::

    There are no drivers installed for MySQL by default, so you need to install the driver you want to use. You can install the ``pymysql`` driver by running the following command:

    .. code-block::
        
        pip install pymysql

PostgreSQL
----------

To connect to a PostgreSQL database, you can use a database string like this:

.. code-block::
    
    postgresql[+driver]://<username>:<password>@<hostname>/<dbname>

Here's an example of a database string that connects to a PostgreSQL database named ``mydatabase`` on a server named ``myserver`` with the username ``myusername`` and the password ``mypassword``. It uses the default PostgreSQL driver (which is ``psycopg2``):

.. code-block::
    
    postgresql://myusername:mypassword@myserver/mydatabase

If you want to create the connection using the ``pg8000 ``, you can use the following database string:

.. code-block::
    
    postgresql+pg8000://myusername:mypassword@myserver/mydatabase

.. important::

    There are no drivers installed for PostgreSQL by default, so you need to install the driver you want to use. You can install the ``pg8000`` driver by running the following command:

    .. code-block::
        
        pip install pg8000
