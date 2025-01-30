from typing import TypedDict

from ..database.operations import Operations


"""
This package encapsulates multiple containers for globally managing dependency injections.

The containers in this package handle the management and injection of dependencies
across various modules, providing a central place to access shared services and components.
"""


    operations: Operations


# Container initialization for database operations services.
container: DatabaseContainer = {"operations": lambda: (Operations)}
