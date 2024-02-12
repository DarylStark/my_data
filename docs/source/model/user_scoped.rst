User scoped models
==================

User scoped models are models that are specific to users, like **User settings** and **Tags**. Every subclass of the ``UserScopedModel`` class is connected to a specific user via the ``user_id`` field. For tokens, we created a extra baseclass with the name ``TokenModel``. The ``User`` class is not particulary a ``UserScopedModel`` model, but since it is imperative to these models, we include it in the ``user_scoped_models`` module.

The following **User Scoped Models** are defined at the moment of writing:

* ``Tag``; represent tags
* ``UserSetting``; represent user settings

The following **Token Models** are defined:

* ``APIClient``; represents API clients defined by a user
* ``APIToken``; represents API tokens for a user

To create a ``UserScoped`` model, use the following syntax:

.. code-block:: python

    from my_model.user_scoped_models import Tag

    tag = Tag(
        title='Holiday',
        color='00ff00')