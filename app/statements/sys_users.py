from pydantic import UUID4
from sqlalchemy import Select, Update, and_, func, update, values

from ..models.sys_users import SysUsers

from ..utilities.data import set_empty_strs_null


class SysUsersStms:
    def __init__(self, model: SysUsers) -> None:
        self._model: SysUsers = model

    @property
    def model(self) -> SysUsers:
        return self._model

    def get_sys_user_by_email(self, email: str) -> Select:
        sys_users = self._model
        return Select(sys_users).where(
            and_(
                sys_users.email == email,
                sys_users.disabled_at == None,
                sys_users.sys_deleted_at == None,
            )
        )

    def get_sys_user_by_username(self, username: str) -> Select:
        sys_users = self._model
        return Select(sys_users).where(
            and_(
                sys_users.username == username,
                sys_users.disabled_at == None,
                sys_users.sys_deleted_at == None,
            )
        )

    def get_sys_user(self, sys_user_uuid: UUID4) -> Select:
        sys_users = self._model
        return Select(sys_users).where(
            and_(
                sys_users.uuid == sys_user_uuid,
                sys_users.disabled_at == None,
                sys_users.sys_deleted_at == None,
            )
        )

    def get_sys_users(self, limit: int, offset: int) -> Select:
        sys_users = self._model
        return (
            Select(sys_users)
            .where(sys_users.sys_deleted_at == None)
            .offset(offset=offset)
            .limit(limit=limit)
        )

    def get_sys_users_ct(self) -> Select:
        sys_users = self._model
        return (
            Select(func.count())
            .select_from(sys_users)
            .where(sys_users.sys_deleted_at == None)
        )

    def update_sys_user(self, sys_user_uuid, sys_user_data: object) -> Update:
        sys_users = self._model
        return (
            update(table=sys_users)
            .where(
                and_(
                    sys_users.uuid == sys_user_uuid,
                    sys_users.disabled_at == None,
                    sys_users.sys_deleted_at == None,
                )
            )
            .values(set_empty_strs_null(values=sys_user_data))
            .returning(sys_users)
        )
