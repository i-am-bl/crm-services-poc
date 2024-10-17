from typing import List

from pydantic import UUID4


class SetField:
    pass

    @staticmethod
    def set_field(new_value: any, old_value: any, data: object) -> any:
        data.old_value = new_value
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
