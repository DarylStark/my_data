"""My Model Package.

This package contains the data model for the complete My application. It
specifies the models that should be used by other packages to create,
retrieve and update items.

The models in this package use the SQLModel class as baseclass so that the
complete validation of Pydantic can be used, and the ORM database structure
of SQLalchemy can be used, without having to use two seperate data schemas.
"""

from .model import *  # noqa: F401, F403

__version__ = '1.3.3'
