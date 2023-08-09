Service users
=============

Using a context to retrieve data is great, but you need a user account to associate the context with. If you are creating a REST API service, for instance, you ned to retrieve the user account first. To do that, the **Service user** exists. A service user cannot have user scoped models like Tags, but does have the permissions to retrieve User objects. It can do this by either using the username for the target user, or by using a API token.

You need to create a ``Context`` object with a Service User to do this and then use a method to retrieve the user object:

.. code-block:: python
    
    # Create the Context for the Service User
    with data_object.get_context_for_service_user(
            username='service.user',
            password='service_password') as context:
        
        # Get the User object by a username
        user = context.get_user_account_by_username('normal.user.1')
        
        # Get the User object by a API toke
        user = context.get_user_account_by_api_token('aRlIytpyz61JX2TvczLxJZUsRzk578pE')

After you've done that, you can use the ``user`` object to create normal ``Contexts`` and retrieve data for the user.