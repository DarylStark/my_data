Using contexts to manipulate data
=================================

After you created a database to work with, you can start using a ``Context`` method to manipulate the data. To create a ``Context`` object, you can use the ``get_context()`` method in the object you've created using the ``MyData`` class. Optionally, you can use the ``Context`` object itself.

.. warning::

    It is always recommended to use the ``get_context()`` method to generate a ``Context`` object. This way, you can be sure that the ``Context`` is correctly bound to the SQLalchmey Database Engine.

The ``Context`` object is a Python context manager. This way, you can use it using the ``with`` statement in Python:

.. code-block:: python

    with data_object.get_context(user=root_user) as context:
        # Perform actions on the context

With the arguments of the ``get_context`` method, you can configure the context in which you are going to manipulate data. At the moment of writing, the only context variable you can specify is the ``User`` object for the user in which the context is run.

The ``Context`` object has a few ``ResourceManagers`` objects to manipulate data in the database:

* ``users``: used to manage users
* ``tags``: used to manage tags
* ``api_clients``: used to manage API clients
* ``api_tokens``: used to manage API tokens
* ``user_settings``: used to manage User Settings

Each ``ResourceManager`` object has four method to manipulate data:

* ``create``: used to create data
* ``retrieve``: used to retrieve data
* ``update``: used to update data
* ``delete``: used to delete data

For example, to create a tag for the user account saved in the ``my_user`` object, you use the following code:

.. code-block:: python

    from my_model.user_scoped_models import Tag

    with data_object.get_context(user=my_user) as context:
        # Create the Tag object
        my_tag = Tag(title='my shiny tag')
        context.tags.create(my_tag)

After doing this, the tag is created in the context for the ``my_user`` user.