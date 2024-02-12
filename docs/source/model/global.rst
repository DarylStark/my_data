Global models
=============

Global Models are models that are used for data that is not bound to a specific user. These models can be used by all users. At the moment of writing, there is only one **Global model**. This is the ``APIScope`` model. This model contains the available API scopes for the API.

API Scope (``APIScope``)
------------------------

API scopes are used to describe available API scopes for API tokens. A API scope is divided into two parts:

* A module, for example ``tags``
* A subject, for example ``retrieve``

The property `full_scope_name` generates a full scope name for the scope. For example ``tags.retrieve``. To create a object of the `APIScope`, use the following code:

.. code-block:: python

    from my_model.global_models import APIScope

    api_scope = APIScope(
        module='tags',
        subject='retrieve')
    
    print(api_scope.full_scope_name)   # Returns: `tags.retrieve`