Authorization
=============

Authorization is the process of determining whether a user has the right to perform a certain action. In the context of a web application, this typically means determining whether a user is allowed to access a certain page or perform a certain action. Within ``MyData``, a user is authorized by the role he has. A root user has the ability to create users, list *all* users, update users and delete users. A normal user can only list and update his own user, but cannot delete of create users. This authorization is done automatically by the ``MyData`` class and you should not have to worry about that.

For services, users should authorize based on other information. One way to authorize is by using ``APIToken`` object. A ``APIToken`` object basically is a password for a user with fine grained permissions. There are two types of ``APIToken`` objects:

-   A short lived ``APIToken``. These tokens can do anything that the user is allowed to do.
-   A long lived ``APIToken``. These tokens can only do what the user is allowed to do and are controlled further by setting specific ``APIScopes``.

To authorize users for these kind of authorization, you can use the ``APITokenAuthorizer`` class.

You can initiate objects from the ``APITokenAuthorizer`` class and use them to authorize users. When creating a object from the ``APITokenAuthorizer`` class, you can specify a ``Authorizer`` object that does the actual authorization. By doing this, you can choose which ``Authorizer`` to use duing runtime. After that, you can use the ``authorize`` method to authorize the user. This method will raise a ``AuthorizationError`` if the user is not authorized.

In this package, there are four authorizers available:

-   ``InvalidTokenAuthorizer``: will authorize for tokens that are not valid. This is useful if you want to authorize the user when he is logged off. For instance, for a logon page.
-   ``ValidTokenAuthorizer``: will authorize for tokens that are valid without looking at any other details. This can be useful for pages that are available to anyone, like info pages.
-   ``ShortLivedTokenAuthorizer``: this will authorize the user if he is using a short lived token.
-   ``APIScopeAuthorizer``: this will authorize the user based on the given scopes to the token.

To use the ``APIScopeAuthorizer``, for example, you use the following code:

.. code-block:: python

    from mytest.authorization import APITokenAuthorizer, APIScopeAuthorizer

    authorizer = APITokenAuthorizer(
        my_data_object=my_data,
        api_token=api_token,
        authorizer=APIScopeAuthorizer(
            required_scopes=['users.retrieve', 'users.create'],
            allow_short_lived=False
        ))
    authorizer.authorize()

This will authorize a API token string if it has the required scopes and is not a short lived token.

Creating own authorizers
------------------------

It is possible to create own authorizers that authorize API tokens based on different information. To do this, create a class that inherits from the ``Authorizer`` class and override the ``authorize`` method. This method should return nothing if the authorization is a success, or raise a ``AuthorizationError`` if the authorization is not a success. You can then pass a instance of the created object to the ``APITokenAuthorizer`` class.