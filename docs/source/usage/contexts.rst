Using contexts to manipulate data
=================================

A context specifies a environment to work in. It also defines a *transaction* in the SQL database. There are two types of ``Context`` objects to work with:

-   ``ServiceContext``: this is the context for **service users** and exposes methods to retrieve ``User`` objects from a username or a ``APItoken`` object.
-   ``UserContext``: this is the contexts for **normal users** and exposes specific ``ResourceManager`` objects that are used to manipulate data. These are for ``User`` objects, ``Tag`` objects, etc.

The ``MyData`` object has two methods to create these kind of contexts:

-   ``get_context``: this method creates a ``UserContext`` object for a specific user. You can use this to manipulate data for a specific user.
-   ``get_context_for_service_user``: this method creates a ``ServiceContext`` object for a specific service user. You can use this to retrieve ``User`` objects from a username or a API token.

Both types of context can and should be used as a Python Context Manager. This means that you can use the ``with`` statement to create a context and automatically close it when you are done. This is the recommended way to use contexts.

The given details for the ``Context`` are placed in a object that is initialized from the ``ContextData`` class.

Using a ``ServiceContext`` object
---------------------------------

the ``ServiceContext`` should be used by a service, like a REST API, to get a specific ``User`` or ``APIToken`` object. The ``ServiceContext`` object exposes three methods that can be used to retrieve specific information:

-   ``get_user_account_by_username``: this method retrieves a ``User`` object from the database by giving a username.
-   ``get_user_account_by_api_token``: this method retrieves a ``User`` object from the database by giving a API token.
-   ``get_api_token_object_by_api_token``: this method retrieves a ``APIToken`` object from the database by giving a API token.

These methods can be used to get a specific user. The given user can in turn be used to create a ``UserContext``. To create a ``ServiceContext`` you use the ``get_context_for_service_user`` method of the ``MyData`` object.

**For example:**

.. code-block:: python
    
    with mydata.get_context_for_service_user(
        username='service.user',
        password='password') as service_context:
        user = service_context.get_user_account_by_username('username')

You now have a ``User`` object that can be used to create a ``UserContext``.

Using a ``UserContext`` object
------------------------------

The ``UserContext`` should be used to manipulate user scoped objects for **normal users**. This includes ``User`` objects, ``Tag`` objects, etc. The ``UserContext`` object exposes specific ``ResourceManager`` objects that are used to manipulate data. These ``ResourceManagers`` objects contain four methods:

-   ``create``: this method creates a new object in the database.
-   ``retrieve``: this method retrieves an object from the database.
-   ``update``: this method updates an object in the database.
-   ``delete``: this method deletes an object from the database.

Each of these methods have a distinct signature that is used to manipulate the data. The specific signatures are described in the documentation of the ``ResourceManager`` objects.

To create a ``UserContext`` object, you can use the ``get_context`` method of the ``MyData`` object. This method requires a ``User`` object to specifiy in what context the given ``UserContext`` should be created. The given ``User`` object can be retrieved from the database by using the ``ServiceContext`` object.

**For example:**


.. code-block:: python
    
    with mydata.get_context(user=user) as user_context:
        # Get all tags for the given user
        tags = user_context.tags.retrieve()