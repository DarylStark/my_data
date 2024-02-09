Using contexts to manipulate data
=================================

A context specifies a environment to work in. It also defines a *transaction* in the SQL database. There are two types of ``Context`` objects to work with:

-   ``ServiceContext``: this is the context for **service users** and exposes methods to retrieve ``User`` objects from a username or a ``APItoken`` object.
-   ``UserContext``: this is the contexts for **normal users** and exposes specific ``ResourceManager`` objects that are used to manipulate data. These are for ``User`` objects, ``Tag`` objects, etc.

The ``MyData`` object has two methods to create these kind of contexts:

-   ``get_context``: this method creates a ``UserContext`` object for a specific user. You can use this to manipulate data for a specific user.
-   ``get_context_for_service_user``: this method creates a ``ServiceContext`` object for a specific service user. You can use this to retrieve ``User`` objects from a username or a API token.

Both types of context can and should be used as a Python Context Manager. This means that you can use the ``with`` statement to create a context and automatically close it when you are done. This is the recommended way to use contexts.

The given details for the ``Context`` are placed in a object that is initialized from the ``ContextData`` class. This includes the ``Session`` object that is used to interact with the database. The ``Session`` object is used to create, retrieve, update and delete data in the database. The ``Session`` object is also used to commit and rollback transactions.

To make this implicit for the user, three methods are added to a ``Context``:

-   ``abort_session``: this method is used to rollback the transaction in the database.
-   ``commit_session``: this method is used to commit the transaction in the database.
-   ``close_session``: this method is used to close the transation in the database.

Using a ``ServiceContext`` object
---------------------------------

the ``ServiceContext`` should be used by a service, like a REST API, to get a specific ``User`` or ``APIToken`` object. The ``ServiceContext`` object exposes four methods that can be used to retrieve specific information:

-   ``get_user_account_by_username``: this method retrieves a ``User`` object from the database by giving a username.
-   ``get_user_account_by_api_token``: this method retrieves a ``User`` object from the database by giving a API token.
-   ``get_api_token_object_by_api_token``: this method retrieves a ``APIToken`` object from the database by giving a API token.
-   ``get_api_token_object_by_api_token``: this method retrieves a ``APIToken`` object from the database by giving a API token.
-   ``get_api_scopes``: this method returns all ``APIScope`` objects that are available in the database.

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

``ResourceManager``'s' in a ``UserContext``
###########################################

The following ``ResourceManagers`` are available in a ``UserContext``:

-   ``api_client``: this ``ResourceManager`` is used to manipulate ``APIClient`` objects.
-   ``api_tokens``: this ``ResourceManager`` is used to manipulate ``APIToken`` objects.
-   ``tags``: this ``ResourceManager`` is used to manipulate ``Tag`` objects.
-   ``user_settings``: this ``ResourceManager`` is used to manipulate ``UserSetting`` objects.
-   ``users``: this ``ResourceManager`` is used to manipulate ``User`` objects.

Creating data
#############

To create data, you use the ``create`` method of any of the given ``ResourceManager`` objects. This method returns a list of the new objects that is created in the database. The ``create`` method only takes the object that should be created as a parameter.

**Example:**

.. code-block:: python

    from my_model import Tag

    tag1 = Tag(name='tag1')
    tag2 = Tag(name='tag2')
    tag3 = Tag(name='tag3')
    tag4 = Tag(name='tag4')

    with mydata.get_context(user=user) as user_context:
        # Create the tags usin a list
        created_tags = user_context.tags.create([tag1, tag2, tag3])

        # Create one tag only
        created_tag = user_context.tags.create(tag4)

You can either give a list of resources to create, or just one single resource. Either way, the ``create`` method returns always a list of the created resources.

Retrieving data
###############

To retrieve data, you use the ``retrieve`` method of any of the ``ResourceManager`` objects. This method returns a list of objects that are retrieved from the database. The ``retrieve`` method has a few parameters that can be used to filter and sort the data that is retrieved. These parameters are:

-   ``flt``: this parameter is used to filter the data that is retrieved. The given filter is a SQLalchemy type filter.
-   ``sort``: this parameter is used to sort the data that is retrieved. The given ``sort`` is a SQLalchemy type ``order_by``.
-   ``start`` and ``max_items``: these parameters are used to paginate the data that is retrieved. The given ``start`` is the index of the first item to retrieve and the given ``max_items`` is the maximum amount of items to retrieve.

**Example:**

.. code-block:: python

    from my_model import Tag

    with mydata.get_context(user=user) as user_context:
        # Retrieve all tags for a user
        all_tags = user_context.tags.retrieve()

        # Retrieve all tags with the word 'work' in it
        work_tags = user_context.tags.retrieve(
            flt=Tag.title.like('%work%')
        )

        # Retrieve all tags for the user, 10 per time, second page
        second_page_tags = user_context.tags.retrieve(start=10, max_items=10)

        # Retrieve all tags for the user, sorted by name
        sorted_tags = user_context.tags.retrieve(sort=Tag.title)

The ``retrieve`` method returns always a list of the retrieved resources, even when only one resource is retrieved.

When you have a resource that has references to other data, such as ``APIScope``'s in a ``APIToken`` object, it is possible that the refered data is not loaded initially. This is because the library uses *lazy loading*. This means that the data is only loaded when it is accessed. To load this data to be able to use it after the context is closed, you have to access it within the Context:

.. code-block:: python

    with mydata.get_context(user=user) as user_context:
        first_token = user_context.api_tokens.retrieve()[0]

        # The `token_scopes` attribute is not loaded yet because of lazy loading, so we
        # have to access it to load it. We don't save it anywhere, but by accessing it,
        # the data is loaded and saved in the `first_token` object. This data is now
        # available after the context is closed.
        _ = first_token.token_scopes

Counting data
#############

Besides of the ``retrieve`` method, the ``ResourceManager`` objects also have a ``count`` method. This method returns the number of records for a specific filter. The ``count`` method takes only a ``flt`` parameter to specify what filter to add to the counting.

**Example:**

.. code-block:: python

    from my_model import Tag

    with mydata.get_context(user=user) as user_context:
        # Retrieve the number of all tags
        all_tags_count = user_context.tags.count()

        # Count all tags with the word 'work' in it
        work_tags_count = user_context.tags.count(
            flt=Tag.title.like('%work%')
        )

.. tip::
    
    Using this method is much more efficient then retrieving all records and counting them in Python. Especially when you want to use pagination, it is recommended to use the ``count`` method to get the total amount of records. This way, you can calculate the amount of pages and the amount of records per page.

Updating data
#############

To update data, you use the ``update`` method of any of the ``ResourceManager`` objects. This method returns a list of the updated objects that are updated in the database. The ``update`` method only takes the objects that should be updated as a parameter. You can either give the object that should be updated, or a list of objects that should be updated.

**Example:**

.. code-block:: python

    from my_model import Tag

    with mydata.get_context(user=user) as user_context:
        # Retrieve a tag
        tag = user_context.tags.retrieve(flt=Tag.title == 'tag1')[0]

        # Update the tag
        tag.title = 'new title'
        updated_tag = user_context.tags.update(tag)

        # Update the tag using a list
        tag1 = user_context.tags.retrieve(flt=Tag.title == 'tag1')[0]
        tag2 = user_context.tags.retrieve(flt=Tag.title == 'tag2')[0]
        tag3 = user_context.tags.retrieve(flt=Tag.title == 'tag3')[0]
        updated_tags = user_context.tags.update([tag1, tag2, tag3])

The ``update`` method returns always a list of the updated resources, even when only one resource is updated.

Deleting data
#############

To delete data, you use the ``delete`` method of any of the ``ResourceManager`` objects. This method doesn't return anything, since the resources are deleted. You can either give the object that should be deleted, or a list of objects that should be deleted.

**Example:**

.. code-block:: python

    from my_model import Tag

    with mydata.get_context(user=user) as user_context:
        # Retrieve a tag
        tag = user_context.tags.retrieve(flt=Tag.title == 'tag1')[0]

        # Delete the tag
        user_context.tags.delete(tag)

        # Delete the tag using a list
        tag1 = user_context.tags.retrieve(flt=Tag.title == 'tag1')[0]
        tag2 = user_context.tags.retrieve(flt=Tag.title == 'tag2')[0]
        tag3 = user_context.tags.retrieve(flt=Tag.title == 'tag3')[0]
        user_context.tags.delete([tag1, tag2, tag3])
