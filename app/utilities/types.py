from typing import Callable, List, TypeVar

from pydantic import UUID4, BaseModel


Schema = TypeVar("T", bound=BaseModel)
