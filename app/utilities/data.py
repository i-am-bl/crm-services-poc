"""
Data utility functions for handling Pydantic model serialization, validation, and object manipulation.

These utilities assist with:
- Serializing Pydantic models to dictionaries.
- Converting unset values to `None`.
- Validating the existence of records and raising appropriate exceptions.
"""

from typing import Callable, List, Optional, TypeVar

from pydantic import UUID4, BaseModel
from .types import Schema
from .logger import logger


def m_dumps(data: object):
    """
    Serializes the given object data into a dictionary representation.

    :param data: The object to serialize.
    :return: dict: A dictionary representation of the object data.
    """
    return data.model_dump()


def m_dumps_unset(data: object):
    """
    Serializes the given object data into a dictionary, excluding unset values.

    :param data: The object to serialize.
    :return: dict: A dictionary representation of the object data with unset values excluded.
    """
    return data.model_dump(exclude_unset=True)


def set_empty_strs_null(values: object):
    """
    Sets empty string fields to None, and ignores optional fields that are None.

    :param values: The object containing the data to process.
    :return: dict: The processed dictionary with empty strings set to None.
    """
    items = values.model_dump(exclude_none=True)
    for key in items:
        if items[key] == "":
            items[key] = None
    return items


def record_exists(instance: object, exception: Exception) -> bool:
    """
    Checks if a record exists and raises the provided exception if it does.

    :param instance: The record instance to check for existence.
    :param exception: The exception to raise if the record exists.
    :return: bool: Returns the instance if it does not exist, raises an exception otherwise.
    """
    if instance:
        class_name = exception.__name__
        logger.warning(
            f"Warning: record already exists, a duplicate entry is not allowed for {class_name}"
        )
        raise exception()
    return instance


def record_not_exist(instance: object, exception: Exception) -> bool:
    """
    Checks if a record does not exist and raises the provided exception if it doesn't.

    :param instance: The record instance to check for non-existence.
    :param exception: The exception to raise if the record does not exist.
    :return: bool: Returns the instance if it exists, raises an exception otherwise.
    """
    if not instance:
        class_name = exception.__name__
        logger.warning(f"Warning: record not found for {class_name}")
        raise exception()
    return instance


def internal_schema_validation(
    schema: Schema,
    setter_method: Callable[
        [
            Schema | List[Schema],
            UUID4,
        ],
        Schema | List[Schema],
    ],
    sys_user_uuid: UUID4,
    data: Schema | List[Schema] | None = None,
) -> Schema | List[Schema]:
    """
    Validates and processes an internal schema by applying a setter method.

    :param data: The input data to be validated, which can be a single instance or a list of instances.
    :param schema: The schema class used for validation and instantiation.
    :param setter_method: A callable function that applies a transformation or metadata update to the schema.
    :param sys_user_uuid: The system user UUID used for setting metadata.

    :return: Schema | List[Schema]: Returns the processed schema instance(s) with applied transformations.
    """
    if isinstance(data, list):
        return [
            setter_method(schema(**item.model_dump()), sys_user_uuid) for item in data
        ]
    elif data == None:
        return setter_method(schema(), sys_user_uuid)
    else:
        return setter_method(schema(**data.model_dump()), sys_user_uuid)
