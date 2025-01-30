from datetime import UTC
from typing import List

from config import settings
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from ..constants import constants as cnst
from ..database.operations import Operations
from ..exceptions import InvalidCredentials, SysUserExists, SysUserNotExist

from ..models.sys_users import SysUsers
from ..schemas.sys_users import (
    SysUsersCreate,
    SysUsersDel,
    SysUsersDelRes,
    SysUsersPgRes,
    SysUsersDisable,
    SysUsersRes,
    SysUsersUpdate,
)
from ..statements.sys_users import SysUsersStms
from ..utilities import pagination
from ..utilities.password import create_hash
from ..utilities.data import record_exists, record_not_exist


class ReadSrvc:
    def __init__(self, statements: SysUsersStms, db_operations: Operations) -> None:
        self._statements: SysUsersStms = statements
        self._db_ops: Operations = db_operations

    @property
    def statements(self) -> SysUsersStms:
        return self._statements

    @property
    def db_operations(self) -> Operations:
        return self._db_ops

    async def get_sys_user(
        self,
        sys_user_uuid: UUID4,
        db: AsyncSession,
    ) -> SysUsersRes:
        statement = self._statements.get_sys_user(sys_user_uuid=sys_user_uuid)
        sys_user = await self._db_ops.return_one_row(
            service=cnst.SYS_USER_READ_SERV, statement=statement, db=db
        )
        return record_not_exist(instance=sys_user, exception=SysUserNotExist)

    async def get_sys_user_by_username(
        self,
        username: str,
        db: AsyncSession,
    ) -> SysUsersRes:
        statement = self._statements.get_sys_user_by_username(username=username)
        sys_user = await self._db_ops.return_one_row(
            service=cnst.SYS_USER_READ_SERV, statement=statement, db=db
        )
        return record_not_exist(instance=sys_user, exception=InvalidCredentials)

    async def get_sys_users(
        self,
        limit: int,
        offset: int,
        db: AsyncSession,
    ) -> List[SysUsersRes]:
        statement = self._statements.get_sys_users(limit=limit, offset=offset)
        sys_users: List[SysUsersRes] = await self._db_ops.return_all_rows(
            service=cnst.SYS_USER_READ_SERV, statement=statement, db=db
        )
        return record_not_exist(instance=sys_users, exception=SysUserNotExist)

    async def get_sys_users_ct(
        self,
        db: AsyncSession,
    ):
        statement = self._statements.get_sys_users_ct()
        return await self._db_ops.return_count(
            service=cnst.SYS_USER_READ_SERV, statement=statement, db=db
        )

    async def paginated_users(
        self, page: int, limit: int, db: AsyncSession
    ) -> SysUsersPgRes:
        total_count = await self.get_sys_users_ct(db=db)
        offset = pagination.page_offset(page=page, limit=limit)
        has_more = pagination.has_more_items(
            total_count=total_count, page=page, limit=limit
        )
        users = await self.get_sys_users(offset=offset, limit=limit, db=db)
        return SysUsersPgRes(
            total=total_count,
            page=page,
            limit=limit,
            has_more=has_more,
            sys_users=users,
        )


class CreateSrvc:
    def __init__(
        self, statements: SysUsersStms, db_operations: Operations, model: SysUsers
    ) -> None:
        self._statements: SysUsersStms = statements
        self._db_ops: Operations = db_operations
        self._model: SysUsers = model

    @property
    def statements(self) -> SysUsersStms:
        return self._statements

    @property
    def db_operations(self) -> Operations:
        return self._db_ops

    @property
    def model(self) -> SysUsers:
        return self._model

    async def create_sys_user(
        self,
        sys_user_data: SysUsersCreate,
        db: AsyncSession,
    ) -> SysUsersRes:
        sys_users = self._model
        statement = self._statements.get_sys_user_by_email(email=sys_user_data.email)
        user_exists: SysUsersRes = await self._db_ops.return_one_row(
            service=cnst.SYS_USER_CREATE_SERV, statement=statement, db=db
        )
        record_exists(instance=user_exists, exception=SysUserExists)
        sys_user_data.password = create_hash(password=sys_user_data.password)
        sys_user: SysUsersRes = await self._db_ops.add_instance(
            service=cnst.SYS_USER_CREATE_SERV,
            model=sys_users,
            data=sys_user_data,
            db=db,
        )
        return record_not_exist(instance=sys_user, exception=SysUserNotExist)


class UpdateSrvc:
    def __init__(self, statements: SysUsersStms, db_operations: Operations) -> None:
        self._statements: SysUsersStms = statements
        self._db_ops: Operations = db_operations

    @property
    def statements(self) -> SysUsersStms:
        return self._statements

    @property
    def db_operations(self) -> Operations:
        return self._db_ops

    async def update_sys_user(
        self,
        sys_user_uuid: UUID4,
        sys_user_data: SysUsersUpdate,
        db: AsyncSession,
    ) -> SysUsersRes:

        statement = self._statements.update_sys_user(
            sys_user_uuid=sys_user_uuid, sys_user_data=sys_user_data
        )
        sys_user: SysUsersRes = await self._db_ops.return_one_row(
            service=cnst.SYS_USER_UPDATE_SERV, statement=statement, db=db
        )
        return record_not_exist(instance=sys_user, exception=SysUserNotExist)

    async def disable_sys_user(
        self,
        sys_user_uuid: UUID4,
        sys_user_data: SysUsersDisable,
        db: AsyncSession,
    ) -> SysUsersDisable:
        statement = self._statements.update_sys_user(
            sys_user_uuid=sys_user_uuid, sys_user_data=sys_user_data
        )
        sys_user: SysUsersDisable = await self._db_ops.return_one_row(
            service=cnst.SYS_USER_UPDATE_SERV, statement=statement, db=db
        )
        return record_not_exist(instance=sys_user, exception=SysUserNotExist)


class DelSrvc:
    def __init__(self, statements: SysUsersStms, db_operations: Operations) -> None:
        self._statements: SysUsersStms = statements
        self._db_ops: Operations = db_operations

    @property
    def statements(self) -> SysUsersStms:
        return self._statements

    @property
    def db_operations(self) -> Operations:
        return self._db_ops

    async def soft_del_sys_user(
        self,
        sys_user_uuid: UUID4,
        sys_user_data: SysUsersDel,
        db: AsyncSession,
    ) -> SysUsersDelRes:
        statement = self._statements.update_sys_user(
            sys_user_uuid=sys_user_uuid, sys_user_data=sys_user_data
        )
        sys_user: SysUsersDelRes = await self._db_ops.return_one_row(
            service=cnst.SYS_USER_UPDATE_SERV, statement=statement, db=db
        )
        return record_not_exist(instance=sys_user, exception=SysUserNotExist)
