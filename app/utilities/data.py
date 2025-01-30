from .logger import logger

"""
Data utility functions for handling Pydantic model serialization, validation, and object manipulation.

These utilities assist with:
- Serializing Pydantic models to dictionaries.
- Converting unset values to `None`.
- Validating the existence of records and raising appropriate exceptions.
"""


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
