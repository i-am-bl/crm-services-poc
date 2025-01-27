from typing import List

from pydantic import UUID4

from ..utilities.logger import logger


class SetField:
    pass

    @staticmethod
    def set_field_value(value: any, field: str, data: object) -> object:
        if hasattr(data, field):
            setattr(data, field, value)
        else:
            logger.warnging(
                f"ValueError: Field: {field} | Data: {data.__class__.__name__}"
            )
            raise ValueError(field)

        return data


class SetSys:
    pass

    @staticmethod
    def sys_created_by(data: object, sys_user: object):
        data.sys_created_by = sys_user.uuid
        return data

    @staticmethod
    def sys_created_by_ls(data: List, sys_user: object):
        for item in data:
            item.sys_created_by = sys_user.uuid
        return data

    @staticmethod
    def sys_updated_by(data: object, sys_user: object):
        data.sys_updated_by = sys_user.uuid
        return data

    @staticmethod
    def sys_updated_by_ls(data: List, sys_user: object):
        for item in data:
            item.sys_created_by = sys_user.uuid
        return data

    @staticmethod
    def sys_deleted_by(data: object, sys_user: object):
        data.sys_deleted_by = sys_user.uuid
        return data

    @staticmethod
    def sys_deleted_by_ls(data: List, sys_user: object):
        for item in data:
            item.sys_created_by = sys_user.uuid
        return data
