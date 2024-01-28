.. my-data documentation master file, created by
   sphinx-quickstart on Mon Jul 31 21:50:46 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to my-data's documentation!
===================================

The ``my-data`` Python library provides the API to save persistent data for the **My Project**. All services in the **My Project** that need to save data needs to use this library to do so. The data is saved in a SQL database using the ``SQLModel`` package. By using the ``my-model`` library, this library makes sure data is saved in a consistent matter.

.. toctree::
   :maxdepth: 2
   :caption: Library usage:
   :numbered:

   usage/installation
   usage/overview
   usage/setup
   usage/contexts
   usage/service_users
   usage/authentication

.. toctree::
   :caption: Developing
   :hidden:
   :maxdepth: 2

   developing/setting_up
   developing/development

.. toctree::
   :caption: API documentation
   :hidden:
   :maxdepth: 2

   api_documentation/class_diagram
   api_documentation/authenticator
   api_documentation/context
   api_documentation/context_data
   api_documentation/creators
   api_documentation/data_manipulator
   api_documentation/deleters
   api_documentation/exceptions
   api_documentation/my_data
   api_documentation/resource_manager
   api_documentation/retrievers
   api_documentation/updaters

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
