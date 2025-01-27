from typing import TypedDict

from ..database.operations import Operations


class DatabaseContainer(TypedDict):
    operations: Operations


container: DatabaseContainer = {"operations": lambda: (Operations)}
