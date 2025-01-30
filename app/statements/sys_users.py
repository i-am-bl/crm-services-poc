from pydantic import UUID4
from sqlalchemy import Select, Update, and_, func, update, values

from ..models.sys_users import SysUsers

from ..utilities.data import set_empty_strs_null


class SysUsersStms:
    """
    A class responsible for constructing SQLAlchemy queries and statements for managing system users (SysUsers).

    ivars:
    ivar: _model: SysUsers: An instance of the SysUsers model.
    """

    def __init__(self, model: SysUsers) -> None:
        """
        Initializes the SysUsersStms class.

        :param model: SysUsers: An instance of the SysUsers model.
        :return: None
        """
        self._model: SysUsers = model

    @property
    def model(self) -> SysUsers:
        """
        Returns the instance of the SysUsers model.

        :return: SysUsers: The SysUsers model instance.
        """
        return self._model

    def get_sys_user_by_email(self, email: str) -> Select:
        """
        Selects a system user by their email.

        :param email: str: The email of the system user.
        :return: Select: A Select statement for the user with the specified email.
        """
        sys_users = self._model
        return Select(sys_users).where(
            and_(
                sys_users.email == email,
                sys_users.disabled_at == None,
                sys_users.sys_deleted_at == None,
            )
        )

    def get_sys_user_by_username(self, username: str) -> Select:
        """
        Selects a system user by their username.

        :param username: str: The username of the system user.
        :return: Select: A Select statement for the user with the specified username.
        """
        sys_users = self._model
        return Select(sys_users).where(
            and_(
                sys_users.username == username,
                sys_users.disabled_at == None,
                sys_users.sys_deleted_at == None,
            )
        )

    def get_sys_user(self, sys_user_uuid: UUID4) -> Select:
        """
        Selects a system user by their UUID.

        :param sys_user_uuid: UUID4: The UUID of the system user.
        :return: Select: A Select statement for the user with the specified UUID.
        """
        sys_users = self._model
        return Select(sys_users).where(
            and_(
                sys_users.uuid == sys_user_uuid,
                sys_users.disabled_at == None,
                sys_users.sys_deleted_at == None,
            )
        )

    def get_sys_users(self, limit: int, offset: int) -> Select:
        """
        Selects system users with pagination support.

        :param limit: int: The maximum number of system users to return.
        :param offset: int: The number of system users to skip.
        :return: Select: A Select statement for system users with pagination.
        """
        sys_users = self._model
        return (
            Select(sys_users)
            .where(sys_users.sys_deleted_at == None)
            .offset(offset=offset)
            .limit(limit=limit)
        )

    def get_sys_users_ct(self) -> Select:
        """
        Selects the count of all system users.

        :return: Select: A Select statement for the count of all system users.
        """
        sys_users = self._model
        return (
            Select(func.count())
            .select_from(sys_users)
            .where(sys_users.sys_deleted_at == None)
        )

    def update_sys_user(self, sys_user_uuid: UUID4, sys_user_data: object) -> Update:
        """
        Updates a system user by their UUID.

        :param sys_user_uuid: UUID4: The UUID of the system user to be updated.
        :param sys_user_data: object: The data to update the system user with.
        :return: Update: An Update statement for the system user.
        """
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
