from datetime import UTC

from config import settings
from fastapi import Depends
from pydantic import UUID4
from sqlalchemy import Select, and_, func, update, values
from sqlalchemy.ext.asyncio import AsyncSession

from ..constants import constants as cnst
from ..database.database import Operations, get_db
from ..exceptions import InvalidCredentials, SysUserExists, SysUserNotExist
from ..models import sys_users as m_sys_user
from ..schemas import sys_users as s_sys_user
from ..utilities.logger import logger
from ..utilities.utilities import DataUtils as di
from ..utilities.utilities import Password


class SysUsersModels:
    sys_users = m_sys_user.SysUsers


class SysUsersStatements:
    pass

    class SelStatements:
        pass

        @staticmethod
        def sel_sys_user_by_email(email: str):
            sys_users = SysUsersModels.sys_users
            statement = Select(sys_users).where(
                and_(
                    sys_users.email == email,
                    sys_users.disabled_at == None,
                    sys_users.sys_deleted_at == None,
                )
            )
            return statement

        @staticmethod
        def sel_sys_user_by_username(username: str):
            sys_users = SysUsersModels.sys_users
            statement = Select(sys_users).where(
                and_(
                    sys_users.username == username,
                    sys_users.disabled_at == None,
                    sys_users.sys_deleted_at == None,
                )
            )
            return statement

        @staticmethod
        def sel_sys_user_by_uuid(sys_user_uuid: UUID4):
            sys_users = SysUsersModels.sys_users
            statement = Select(sys_users).where(
                and_(
                    sys_users.uuid == sys_user_uuid,
                    sys_users.disabled_at == None,
                    sys_users.sys_deleted_at == None,
                )
            )
            return statement

        @staticmethod
        def sel_sys_users(limit: int, offset: int):
            sys_users = SysUsersModels.sys_users
            statement = (
                Select(sys_users)
                .where(sys_users.sys_deleted_at == None)
                .offset(offset=offset)
                .limit(limit=limit)
            )
            return statement

        @staticmethod
        def sel_sys_users_ct():
            sys_users = SysUsersModels.sys_users
            statement = (
                Select(func.count())
                .select_from(sys_users)
                .where(sys_users.sys_deleted_at == None)
            )
            return statement

    class UpdateStatements:
        def __init__(self) -> None:
            pass

        def update_sys_user_by_uuid(sys_user_uuid, sys_user_data: object):
            sys_users = SysUsersModels.sys_users
            statement = (
                update(table=sys_users)
                .where(
                    and_(
                        sys_users.uuid == sys_user_uuid,
                        sys_users.disabled_at == None,
                        sys_users.sys_deleted_at == None,
                    )
                )
                .values(di.set_empty_strs_null(values=sys_user_data))
                .returning(sys_users)
            )
            return statement


class SysUsersServices:
    pass

    class ReadService:
        def __init__(self) -> None:
            pass

        async def get_sys_user_by_uuid(
            self,
            sys_user_uuid: UUID4,
            db: AsyncSession = Depends(get_db),
        ):
            statement = SysUsersStatements.SelStatements.sel_sys_user_by_uuid(
                sys_user_uuid=sys_user_uuid
            )
            sys_user = await Operations.return_one_row(
                service=cnst.SYS_USER_READ_SERV, statement=statement, db=db
            )
            return di.record_not_exist(instance=sys_user, exception=SysUserNotExist)

        async def get_sys_user_by_username(
            self,
            username: str,
            db: AsyncSession = Depends(get_db),
        ):
            statement = SysUsersStatements.SelStatements.sel_sys_user_by_username(
                username=username
            )
            sys_user = await Operations.return_one_row(
                service=cnst.SYS_USER_READ_SERV, statement=statement, db=db
            )
            return di.record_not_exist(instance=sys_user, exception=InvalidCredentials)

        async def get_sys_users(
            self,
            limit: int,
            offset: int,
            db: AsyncSession = Depends(get_db),
        ):
            statement = SysUsersStatements.SelStatements.sel_sys_users(
                limit=limit, offset=offset
            )
            sys_users = await Operations.return_all_rows(
                service=cnst.SYS_USER_READ_SERV, statement=statement, db=db
            )
            return di.record_not_exist(instance=sys_users, exception=SysUserNotExist)

        async def get_sys_users_ct(
            self,
            db: AsyncSession = Depends(get_db),
        ):
            statement = SysUsersStatements.SelStatements.sel_sys_users_ct()
            return await Operations.return_count(
                service=cnst.SYS_USER_READ_SERV, statement=statement, db=db
            )

    class CreateService:
        def __init__(self) -> None:
            pass

        async def create_sys_user(
            self,
            sys_user_data: s_sys_user.SysUsersCreate,
            db: AsyncSession = Depends(get_db),
        ):
            sys_users = SysUsersModels.sys_users
            statement = SysUsersStatements.SelStatements.sel_sys_user_by_email(
                email=sys_user_data.email
            )
            user_exists = await Operations.return_one_row(
                service=cnst.SYS_USER_CREATE_SERV, statement=statement, db=db
            )
            di.record_exists(instance=user_exists, exception=SysUserExists)
            sys_user_data.password = Password.create_hash(
                password=sys_user_data.password
            )
            sys_user = await Operations.add_instance(
                service=cnst.SYS_USER_CREATE_SERV,
                model=sys_users,
                data=sys_user_data,
                db=db,
            )
            return di.record_not_exist(instance=sys_user, exception=SysUserNotExist)

    class UpdateService:
        async def update_sys_user(
            self,
            sys_user_uuid: UUID4,
            sys_user_data: s_sys_user.SysUsersUpdate,
            db: AsyncSession = Depends(get_db),
        ):

            statement = SysUsersStatements.UpdateStatements.update_sys_user_by_uuid(
                sys_user_uuid=sys_user_uuid, sys_user_data=sys_user_data
            )
            sys_user = await Operations.return_one_row(
                service=cnst.SYS_USER_UPDATE_SERV, statement=statement, db=db
            )
            return di.record_not_exist(instance=sys_user, exception=SysUserNotExist)

        async def disable_sys_user(
            self,
            sys_user_uuid: UUID4,
            sys_user_data: s_sys_user.SysUsersDisable,
            db: AsyncSession = Depends(get_db),
        ):
            statement = SysUsersStatements.UpdateStatements.update_sys_user_by_uuid(
                sys_user_uuid=sys_user_uuid, sys_user_data=sys_user_data
            )
            sys_user = await Operations.return_one_row(
                service=cnst.SYS_USER_UPDATE_SERV, statement=statement, db=db
            )
            return di.record_not_exist(instance=sys_user, exception=SysUserNotExist)

    class DelService:
        async def soft_del_sys_user(
            self,
            sys_user_uuid: UUID4,
            sys_user_data: s_sys_user.SysUsersDel,
            db: AsyncSession = Depends(get_db),
        ):
            statement = SysUsersStatements.UpdateStatements.update_sys_user_by_uuid(
                sys_user_uuid=sys_user_uuid, sys_user_data=sys_user_data
            )
            sys_user = await Operations.return_one_row(
                service=cnst.SYS_USER_UPDATE_SERV, statement=statement, db=db
            )
            return di.record_not_exist(instance=sys_user, exception=SysUserNotExist)
