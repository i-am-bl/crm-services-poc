from typing import TypedDict

from ..database.operations import Operations


class DatabaseContainer(TypedDict):
    """
    A container that holds dependencies related to database operations.

    This container is used to manage and inject dependencies for database-related operations.
    """

    operations: Operations


# Container initialization for database operations services.
container: DatabaseContainer = {"operations": lambda: Operations}
