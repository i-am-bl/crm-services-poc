from typing import List

from pydantic import UUID4

from ..models import sys_users as sys_users_mdl


def sys_created_by(data: object, sys_user: sys_users_mdl.SysUsers) -> object:
    data.sys_created_by = sys_user.uuid
    return data


def sys_created_by_ls(data: List, sys_user: sys_users_mdl.SysUsers) -> object:
    for item in data:
        item.sys_created_by = sys_user.uuid
    return data


def sys_updated_by(data: object, sys_user: sys_users_mdl.SysUsers) -> object:
    data.sys_updated_by = sys_user.uuid
    return data


def sys_updated_by_ls(data: List, sys_user: sys_users_mdl.SysUsers) -> object:
    for item in data:
        item.sys_created_by = sys_user.uuid
    return data


def sys_deleted_by(data: object, sys_user: sys_users_mdl.SysUsers) -> object:
    data.sys_deleted_by = sys_user.uuid
    return data


def sys_deleted_by_ls(data: List, sys_user: sys_users_mdl.SysUsers) -> object:
    for item in data:
        item.sys_created_by = sys_user.uuid
    return data
