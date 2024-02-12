.. my-data documentation master file, created by
   sphinx-quickstart on Mon Jul 31 21:50:46 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to my-data's documentation!
===================================

The ``my-data`` Python library provides the API to save persistent data for the **My Project**. All services in the **My Project** that need to save data needs to use this library to do so. The data is saved in a SQL database using the ``SQLModel`` package. By using the ``my-model`` library, this library makes sure data is saved in a consistent matter.

.. toctree::
   :maxdepth: 3
   :caption: Library usage:
   :numbered:

   usage/installation
   usage/overview
   usage/setup
   usage/contexts
   usage/authentication
   usage/authorization

.. toctree::
   :caption: Examples
   :maxdepth: 2

   examples/rest_api_service_example

.. toctree::
   :caption: Useful information
   :maxdepth: 2

   useful_information/database_string_examples

.. toctree::
   :caption: Model
   :maxdepth: 2

   model/index
   model/global
   model/user_scoped

.. toctree::
   :caption: Developing
   :hidden:
   :maxdepth: 2

   developing/setting_up
   developing/development

.. toctree::
   :caption: My Data - API documentation
   :hidden:
   :maxdepth: 2

   api_documentation/my_data/authenticator
   api_documentation/my_data/authorizer
   api_documentation/my_data/context
   api_documentation/my_data/context_data
   api_documentation/my_data/creators
   api_documentation/my_data/data_loader
   api_documentation/my_data/data_manipulator
   api_documentation/my_data/deleters
   api_documentation/my_data/exceptions
   api_documentation/my_data/my_data
   api_documentation/my_data/my_data_table_creator
   api_documentation/my_data/resource_manager
   api_documentation/my_data/retrievers
   api_documentation/my_data/updaters

.. toctree::
   :caption: My Model - API documentation
   :hidden:
   :maxdepth: 2

   api_documentation/my_model/model

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
