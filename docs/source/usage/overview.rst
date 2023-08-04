Overview
========

The main class for the library is the ``MyData`` class. This class should be initiated to use the ``my-data`` package and contains a method to retrieve a ``Context`` object. The ``Context`` object is used to interact with the database in a specific context. A context defines which user is requesting the data manipulation. By using this context, you can make sure the user that is trying to do something, is allowed to do this.

To initiate a object of the ``MyData`` class, you should use the following syntax:

.. code-block:: python

    from my_data.my_data import MyData

    data_object = MyData()

Once you've done this, you can configure the object with the ``.configure`` method. After that, you can create the engine and, optionally, create the tables and initialization data.