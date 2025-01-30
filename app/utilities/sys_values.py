from typing import List, Literal, Callable
from pydantic import UUID4

SysFieldSetter = Callable[[object | List[object], UUID4], object | List[object]]

"""
sys_values utilities provide reusable setter methods for system fields. These utilities manage
the injection of user-related information (such as creation, update, or deletion) on objects or 
lists of objects during I/O operations.
"""


def set_sys_field(
    data: object | List[object],
    field: Literal["sys_created_by", "sys_updated_by", "sys_deleted_by"],
    value: UUID4,
) -> object | List[object]:
    """
    Helper function to set the sys_created_by on a single object or list of objects.

    :param data: An object or list of objects that needs to be updated with user that has taken action.
    :type data: object | List[object]
    :param field: System user reference field.
    :type field: Literal["sys_created_by", "sys_updated_by", "sys_deleted_by"]
    :return: The update object or list of objects.
    :rtype: object | List[object]

    """
    if isinstance(data, list):
        for item in data:
            setattr(item, field, value)
    else:
        setattr(data, field, value)
    return data


def sys_created_by(
    data: object | List[object], sys_user_uuid: UUID4
) -> object | List[object]:
    """
    Utility function to set the sys_created_by on a single object or list of objects.

    :param data: object | List[object]: The object or list of objects to update.
    :param sys_user: UUID4: The system user performing the operation.
    :return: object | List[object]: The updated object or list of objects
    """
    return set_sys_field(data=data, field="sys_created_by", value=sys_user_uuid)


def sys_updated_by(
    data: object | List[object], sys_user_uuid: UUID4
) -> object | List[object]:
    """
    Utility function to set the sys_updated_by on a single object or list of objects.

    :param data: object | List[object]: The object or list of objects to update.
    :param sys_user: UUID4: The system user performing the operation.
    :return: object | List[object]: The updated object or list of objects
    """
    return set_sys_field(data=data, field="sys_updated_by", value=sys_user_uuid)


def sys_deleted_by(
    data: object | List[object], sys_user_uuid: UUID4
) -> object | List[object]:
    """
    Utility function to set the sys_deleted_by on a single object or list of objects.

    :param data: object | List[object]: The object or list of objects to update.
    :param sys_user: UUID4: The system user performing the operation.
    :return: object | List[object]: The updated object or list of objects
    """
    return set_sys_field(data=data, field="sys_deleted_by", value=sys_user_uuid)
