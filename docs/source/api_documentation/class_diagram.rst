Class diagram
=============

This page describes, by using a UML diagram, the relations every class has with other classes.

``MyData``
----------

The ``MyData`` class is the main class for the library and is the only class that should be directly initialized.

.. mermaid::

   classDiagram

   class MyData

   MyData: Engine database_engine
   MyData: str _database_str
   MyData: dict[str, Any] _database_args
   MyData: none configure()
   MyData: none create_db_tables()
   MyData: none creat_engine()
   MyData: create_init_data()
   MyData: Cotnext get_context()

``Context`` and ``ContextData``
-------------------------------

The ``ContextData`` and ``Context`` classes are used to create a context for a specific use case. The ``Context`` class uses the ``ContextData`` to defined in what context to operate. The ``Context`` class exposes a few ``DataManipulator`` classes to give the end user the option to manipulate data.

.. mermaid::

   classDiagram

   class Context
   class ContextData

   ContextData *-- Context : _context_data

   Context: Engine database_engine
   Context: ContextData _context_data

   ContextData: User user

``DataManipulator``
-------------------

The ``DataManipulator`` classes are used to create, retrieve, update or delete data.

.. mermaid::

   classDiagram

   DataManipulator <|-- Creator
   DataManipulator <|-- Deleter
   DataManipulator <|-- Retriever
   DataManipulator <|-- Updater

   Creator <|-- UserCreator
   Creator <|-- UserScopedCreator

   Deleter <|-- UserDeleter
   Deleter <|-- UserScopedDeleter

   Retriever <|-- UserRetriever
   Retriever <|-- UserScopedRetriever

   Updater <|-- UserUpdater
   Updater <|-- UserScopedUpdater

   DataManipulator: SQLMdodel _database_model
   DataManipulator: Engine _database_engine
   DataManipulator: ContextData _context_data
   DataManipulator: list _convert_model_to_list()
   DataManipulator: list _validate_user_scoped_models()
   DataManipulator: list _add_models_to_session()

   Creator: bool is_authorized()
   Creator: list create()
   UserCreator: bool is_authorized()
   UserCreator: list create()
   UserScopedCreator: bool is_authorized()

   Deleter: none delete()
   UserDeleter: none delete()
   UserScopedDeleter: none delete()

   Retriever: list get_context_filters()
   Retriever: list retrieve()
   UserRetriever: list get_context_filters()
   UserScopedRetriever: list get_context_filters()

   Updater: list update
   UserUpdater: list update
   UserScopedUpdater: list update

The following pages describe the API for this library.