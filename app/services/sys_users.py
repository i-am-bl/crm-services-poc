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
    """
    Service for retrieving system user entries from the database.

    This class provides functionality for reading system users' information,
    including fetching single users by UUID or username, retrieving paginated lists of users,
    and counting the total number of system users.

    :param statements: The SQL statements used for system user-related queries.
    :type statements: SysUsersStms
    :param db_operations: The database operations object used for executing queries.
    :type db_operations: Operations
    """

    def __init__(self, statements: SysUsersStms, db_operations: Operations) -> None:
        """
        Initializes the ReadSrvc class with the provided SQL statements and database operations.

        :param statements: The SQL statements used for system user-related queries.
        :type statements: SysUsersStms
        :param db_operations: The database operations object used for executing queries.
        :type db_operations: Operations
        """
        self._statements: SysUsersStms = statements
        self._db_ops: Operations = db_operations

    @property
    def statements(self) -> SysUsersStms:
        """
        Returns the instance of SysUsersStms.

        :returns: The SQL statements handler for system users.
        :rtype: SysUsersStms
        """
        return self._statements

    @property
    def db_operations(self) -> Operations:
        """
        Returns the instance of Operations.

        :returns: The database operations handler.
        :rtype: Operations
        """
        return self._db_ops

    async def get_sys_user(
        self,
        sys_user_uuid: UUID4,
        db: AsyncSession,
    ) -> SysUsersRes:
        """
        Retrieves a system user from the database by their UUID.

        :param sys_user_uuid: The UUID of the system user to retrieve.
        :type sys_user_uuid: UUID4
        :param db: The asynchronous session for database operations.
        :type db: AsyncSession

        :returns: The retrieved system user.
        :rtype: SysUsersRes
        :raises SysUserNotExist: If no system user is found with the given UUID.
        """
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
        """
        Retrieves a system user from the database by their username.

        :param username: The username of the system user to retrieve.
        :type username: str
        :param db: The asynchronous session for database operations.
        :type db: AsyncSession

        :returns: The retrieved system user.
        :rtype: SysUsersRes
        :raises InvalidCredentials: If no system user is found with the given username.
        """
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
        """
        Retrieves a list of system users with pagination support.

        :param limit: The maximum number of users to retrieve.
        :type limit: int
        :param offset: The offset for pagination.
        :type offset: int
        :param db: The asynchronous session for database operations.
        :type db: AsyncSession

        :returns: A list of system users.
        :rtype: List[SysUsersRes]
        :raises SysUserNotExist: If no system users are found.
        """
        statement = self._statements.get_sys_users(limit=limit, offset=offset)
        sys_users: List[SysUsersRes] = await self._db_ops.return_all_rows(
            service=cnst.SYS_USER_READ_SERV, statement=statement, db=db
        )
        return record_not_exist(instance=sys_users, exception=SysUserNotExist)

    async def get_sys_users_ct(
        self,
        db: AsyncSession,
    ):
        """
        Retrieves the total count of system users.

        :param db: The asynchronous session for database operations.
        :type db: AsyncSession

        :returns: The total count of system users.
        :rtype: int
        """
        statement = self._statements.get_sys_users_ct()
        return await self._db_ops.return_count(
            service=cnst.SYS_USER_READ_SERV, statement=statement, db=db
        )

    async def paginated_users(
        self, page: int, limit: int, db: AsyncSession
    ) -> SysUsersPgRes:
        """
        Retrieves a paginated list of system users, including the total count and pagination information.

        :param page: The current page number for pagination.
        :type page: int
        :param limit: The maximum number of users per page.
        :type limit: int
        :param db: The asynchronous session for database operations.
        :type db: AsyncSession

        :returns: The paginated list of system users.
        :rtype: SysUsersPgRes
        """
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
    """
    Service for creating new system users in the database.

    This class provides functionality for creating new system users, including checking for existing
    users with the same email, hashing the password, and adding the user to the database.

    :param statements: The SQL statements used for system user-related queries.
    :type statements: SysUsersStms
    :param db_operations: The database operations object used for executing queries.
    :type db_operations: Operations
    :param model: The model class representing the system user entity.
    :type model: SysUsers
    """

    def __init__(
        self,
        statements: SysUsersStms,
        db_operations: Operations,
        model: SysUsers,
    ) -> None:
        """
        Initializes the CreateSrvc class with the provided SQL statements, database operations, and model.

        :param statements: The SQL statements used for system user-related queries.
        :type statements: SysUsersStms
        :param db_operations: The database operations object used for executing queries.
        :type db_operations: Operations
        :param model: The model class representing the system user entity.
        :type model: SysUsers
        """
        self._statements: SysUsersStms = statements
        self._db_ops: Operations = db_operations
        self._model: SysUsers = model

    @property
    def statements(self) -> SysUsersStms:
        """
        Returns the instance of SysUsersStms.

        :returns: The SQL statements handler for system user-related queries.
        :rtype: SysUsersStms
        """
        return self._statements

    @property
    def db_operations(self) -> Operations:
        """
        Returns the instance of Operations.

        :returns: The database operations handler.
        :rtype: Operations
        """
        return self._db_ops

    @property
    def model(self) -> SysUsers:
        """
        Returns the model class representing system users.

        :returns: The model class for system users.
        :rtype: SysUsers
        """
        return self._model

    async def create_sys_user(
        self,
        sys_user_data: SysUsersCreate,
        db: AsyncSession,
    ) -> SysUsersRes:
        """
        Creates a new system user in the database.

        This method performs the following steps:
        1. Checks if a system user already exists with the same email.
        2. Hashes the user's password.
        3. Adds the new user to the database.

        :param sys_user_data: The data to create the new system user.
        :type sys_user_data: SysUsersCreate
        :param db: The asynchronous session for database operations.
        :type db: AsyncSession

        :returns: The newly created system user.
        :rtype: SysUsersRes
        :raises SysUserExists: If a system user with the same email already exists.
        :raises SysUserNotExist: If the newly created user does not exist after insertion.
        """
        sys_users = self._model
        # Check if the user already exists by email
        statement = self._statements.get_sys_user_by_email(email=sys_user_data.email)
        user_exists: SysUsersRes = await self._db_ops.return_one_row(
            service=cnst.SYS_USER_CREATE_SERV, statement=statement, db=db
        )
        record_exists(instance=user_exists, exception=SysUserExists)

        # Hash the password before saving
        sys_user_data.password = create_hash(password=sys_user_data.password)

        # Create the new system user in the database
        sys_user: SysUsersRes = await self._db_ops.add_instance(
            service=cnst.SYS_USER_CREATE_SERV,
            model=sys_users,
            data=sys_user_data,
            db=db,
        )

        return record_not_exist(instance=sys_user, exception=SysUserNotExist)


class UpdateSrvc:
    """
    Service for updating and disabling system users in the database.

    This class provides functionality for updating system users' information, including enabling
    and disabling user accounts.

    :param statements: The SQL statements used for system user-related queries.
    :type statements: SysUsersStms
    :param db_operations: The database operations object used for executing queries.
    :type db_operations: Operations
    """

    def __init__(self, statements: SysUsersStms, db_operations: Operations) -> None:
        """
        Initializes the UpdateSrvc class with the provided SQL statements and database operations.

        :param statements: The SQL statements used for system user-related queries.
        :type statements: SysUsersStms
        :param db_operations: The database operations object used for executing queries.
        :type db_operations: Operations
        """
        self._statements: SysUsersStms = statements
        self._db_ops: Operations = db_operations

    @property
    def statements(self) -> SysUsersStms:
        """
        Returns the instance of SysUsersStms.

        :returns: The SQL statements handler for system user-related queries.
        :rtype: SysUsersStms
        """
        return self._statements

    @property
    def db_operations(self) -> Operations:
        """
        Returns the instance of Operations.

        :returns: The database operations handler.
        :rtype: Operations
        """
        return self._db_ops

    async def update_sys_user(
        self,
        sys_user_uuid: UUID4,
        sys_user_data: SysUsersUpdate,
        db: AsyncSession,
    ) -> SysUsersRes:
        """
        Updates an existing system user in the database.

        This method updates the information of an existing system user identified by `sys_user_uuid`.

        :param sys_user_uuid: The UUID of the system user to update.
        :type sys_user_uuid: UUID4
        :param sys_user_data: The new data to update the system user.
        :type sys_user_data: SysUsersUpdate
        :param db: The asynchronous session for database operations.
        :type db: AsyncSession

        :returns: The updated system user.
        :rtype: SysUsersRes
        :raises SysUserNotExist: If the system user with the specified UUID does not exist.
        """
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
        """
        Disables an existing system user in the database.

        This method disables the system user account identified by `sys_user_uuid`.

        :param sys_user_uuid: The UUID of the system user to disable.
        :type sys_user_uuid: UUID4
        :param sys_user_data: The data indicating the system user's status (disabled).
        :type sys_user_data: SysUsersDisable
        :param db: The asynchronous session for database operations.
        :type db: AsyncSession

        :returns: The disabled system user.
        :rtype: SysUsersDisable
        :raises SysUserNotExist: If the system user with the specified UUID does not exist.
        """
        statement = self._statements.update_sys_user(
            sys_user_uuid=sys_user_uuid, sys_user_data=sys_user_data
        )
        sys_user: SysUsersDisable = await self._db_ops.return_one_row(
            service=cnst.SYS_USER_UPDATE_SERV, statement=statement, db=db
        )
        return record_not_exist(instance=sys_user, exception=SysUserNotExist)


class DelSrvc:
    """
    Service for soft-deleting system users in the database.

    This class provides functionality for soft-deleting system users, effectively marking them
    as deleted rather than permanently removing them from the database.

    :param statements: The SQL statements used for system user-related queries.
    :type statements: SysUsersStms
    :param db_operations: The database operations object used for executing queries.
    :type db_operations: Operations
    """

    def __init__(self, statements: SysUsersStms, db_operations: Operations) -> None:
        """
        Initializes the DelSrvc class with the provided SQL statements and database operations.

        :param statements: The SQL statements used for system user-related queries.
        :type statements: SysUsersStms
        :param db_operations: The database operations object used for executing queries.
        :type db_operations: Operations
        """
        self._statements: SysUsersStms = statements
        self._db_ops: Operations = db_operations

    @property
    def statements(self) -> SysUsersStms:
        """
        Returns the instance of SysUsersStms.

        :returns: The SQL statements handler for system user-related queries.
        :rtype: SysUsersStms
        """
        return self._statements

    @property
    def db_operations(self) -> Operations:
        """
        Returns the instance of Operations.

        :returns: The database operations handler.
        :rtype: Operations
        """
        return self._db_ops

    async def soft_del_sys_user(
        self,
        sys_user_uuid: UUID4,
        sys_user_data: SysUsersDel,
        db: AsyncSession,
    ) -> SysUsersDelRes:
        """
        Soft-deletes a system user by marking them as deleted in the database.

        This method will update the system user's status to "deleted" rather than removing them
        from the database.

        :param sys_user_uuid: The UUID of the system user to soft-delete.
        :type sys_user_uuid: UUID4
        :param sys_user_data: The data indicating the system user's status (deleted).
        :type sys_user_data: SysUsersDel
        :param db: The asynchronous session for database operations.
        :type db: AsyncSession

        :returns: The system user marked as deleted.
        :rtype: SysUsersDelRes
        :raises SysUserNotExist: If the system user with the specified UUID does not exist.
        """
        statement = self._statements.update_sys_user(
            sys_user_uuid=sys_user_uuid, sys_user_data=sys_user_data
        )
        sys_user: SysUsersDelRes = await self._db_ops.return_one_row(
            service=cnst.SYS_USER_UPDATE_SERV, statement=statement, db=db
        )
        return record_not_exist(instance=sys_user, exception=SysUserNotExist)
