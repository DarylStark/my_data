"""The updaters for the ResourceMAaager.

This module contains the Updaters for the ResourceManager. It contains the
base-class and the subclasses.
"""

from .crud_base import CRUDBase


class Updater(CRUDBase):
    """Base Updater class.

    The base Updater class should be used as the base class for specific
    Updater-classes. The base class defines the interface for all
    Updater-classes.
    """


class UserSpecificUpdater(Updater):
    """Updater for user specific resources.

    This updater should be used for resources that are bound to specific users,
    like tags and API tokens.
    """


class UserUpdater(Updater):
    """Updatar for user resources.

    This updater should be used to updater users.
    """
