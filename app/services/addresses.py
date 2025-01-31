from typing import Literal, List

from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from ..constants import constants as cnst
from ..database.operations import Operations
from ..exceptions import AddressExists, AddressNotExist
from ..models.addresses import Addresses
from ..schemas.addresses import (
    AccountAddressesCreate,
    AccountAddressesInternalCreate,
    EntityAddressesCreate,
    AddressesDel,
    AddressesDelRes,
    AddressesPgRes,
    AddressesRes,
    AddressesUpdate,
    EntityAddressesInternalCreate,
)
from ..statements.addresses import AddressesStms
from ..utilities import pagination
from ..utilities.data import record_not_exist, record_exists


class ReadSrvc:
    """
    Service for reading addresses from the database.

    This class provides functionality to retrieve address data from the database,
    including fetching a single address, a list of addresses, and performing pagination.

    :param statements: The SQL statements used for retrieving address data.
    :type statements: AddressesStms
    :param db_operations: The database operations object used for executing queries.
    :type db_operations: Operations
    """

    def __init__(self, statements: AddressesStms, db_operations: Operations) -> None:
        """
        Initializes the ReadSrvc class with the provided statements and database operations.

        :param statements: The SQL statements used for retrieving address data.
        :type statements: AddressesStms
        :param db_operations: The database operations object used for executing queries.
        :type db_operations: Operations
        """
        self._statements: AddressesStms = statements
        self._db_ops: Operations = db_operations

    @property
    def statements(self) -> Addresses:
        """
        Returns the addresses SQL statements.

        :return: The addresses SQL statements.
        :rtype: AddressesStms
        """
        return self._statements

    @property
    def db_operations(self) -> Operations:
        """
        Returns the database operations object.

        :return: The database operations object.
        :rtype: Operations
        """
        return self._db_ops

    async def get_address(
        self,
        parent_uuid: UUID4,
        parent_table: Literal["entities", "accounts"],
        address_uuid: UUID4,
        db: AsyncSession,
    ) -> AddressesRes:
        """
        Retrieves a specific address from the database based on the given UUID.

        :param parent_uuid: The UUID of the parent (either an entity or an account).
        :type parent_uuid: UUID4
        :param parent_table: The table the address is associated with, either "entities" or "accounts".
        :type parent_table: Literal["entities", "accounts"]
        :param address_uuid: The UUID of the address to retrieve.
        :type address_uuid: UUID4
        :param db: The database session.
        :type db: AsyncSession
        :return: The retrieved address.
        :rtype: AddressesRes
        :raises AddressNotExist: If the address does not exist.
        """
        statement = self._statements.get_address(
            parent_uuid=parent_uuid,
            address_uuid=address_uuid,
            parent_table=parent_table,
        )
        address: AddressesRes = await self._db_ops.return_one_row(
            service=cnst.ADDRESSES_READ_SERVICE, statement=statement, db=db
        )
        return record_not_exist(instance=address, exception=AddressNotExist)

    async def get_addresses(
        self,
        parent_uuid: UUID4,
        parent_table: Literal["entities", "accounts"],
        limit: int,
        offset: int,
        db: AsyncSession,
    ) -> List[AddressesRes]:
        """
        Retrieves a list of addresses for a specific parent (entity or account).

        :param parent_uuid: The UUID of the parent (either an entity or an account).
        :type parent_uuid: UUID4
        :param parent_table: The table the addresses are associated with, either "entities" or "accounts".
        :type parent_table: Literal["entities", "accounts"]
        :param limit: The maximum number of addresses to return.
        :type limit: int
        :param offset: The starting point for the query (used for pagination).
        :type offset: int
        :param db: The database session.
        :type db: AsyncSession
        :return: A list of addresses.
        :rtype: List[AddressesRes]
        :raises AddressNotExist: If no addresses exist for the given parent.
        """
        statement = self._statements.get_address_by_entity(
            parent_uuid=parent_uuid,
            parent_table=parent_table,
            offset=offset,
            limit=limit,
        )
        addresses: List[AddressesRes] = await self._db_ops.return_all_rows(
            service=cnst.ADDRESSES_READ_SERVICE, statement=statement, db=db
        )
        return record_not_exist(instance=addresses, exception=AddressNotExist)

    async def get_addresses_ct(
        self,
        parent_uuid: UUID4,
        parent_table: Literal["entities", "accounts"],
        db: AsyncSession,
    ) -> int:
        """
        Retrieves the count of addresses for a specific parent (entity or account).

        :param parent_uuid: The UUID of the parent (either an entity or an account).
        :type parent_uuid: UUID4
        :param parent_table: The table the addresses are associated with, either "entities" or "accounts".
        :type parent_table: Literal["entities", "accounts"]
        :param db: The database session.
        :type db: AsyncSession
        :return: The total count of addresses for the given parent.
        :rtype: int
        """
        statement = self._statements.get_addresses_ct(
            parent_uuid=parent_uuid, parent_table=parent_table
        )
        return await self._db_ops.return_count(
            service=cnst.ADDRESSES_READ_SERVICE, statement=statement, db=db
        )

    async def paginated_addresses(
        self,
        parent_uuid: UUID4,
        parent_table: Literal["entities", "accounts"],
        limit: int,
        page: int,
        db: AsyncSession,
    ) -> AddressesPgRes:
        """
        Retrieves paginated addresses for a specific parent (entity or account).

        :param parent_uuid: The UUID of the parent (either an entity or an account).
        :type parent_uuid: UUID4
        :param parent_table: The table the addresses are associated with, either "entities" or "accounts".
        :type parent_table: Literal["entities", "accounts"]
        :param limit: The maximum number of addresses per page.
        :type limit: int
        :param page: The page number for pagination.
        :type page: int
        :param db: The database session.
        :type db: AsyncSession
        :return: A paginated result of addresses.
        :rtype: AddressesPgRes
        """
        total_count = await self.get_addresses_ct(
            parent_uuid=parent_uuid, parent_table=parent_table, db=db
        )
        offset = pagination.page_offset(page=page, limit=limit)
        has_more = pagination.has_more_items(
            total_count=total_count, page=page, limit=limit
        )
        addresses = await self.get_addresses(
            parent_uuid=parent_uuid,
            parent_table=parent_table,
            offset=offset,
            limit=limit,
            db=db,
        )
        return AddressesPgRes(
            total=total_count,
            page=page,
            limit=limit,
            has_more=has_more,
            addresses=addresses,
        )


class CreateSrvc:
    """
    Service for creating addresses in the database.

    This class provides functionality to create new address records in the database.

    :param statements: The SQL statements used for creating address data.
    :type statements: AddressesStms
    :param db_operations: The database operations object used for executing queries.
    :type db_operations: Operations
    :param model: The address model for creating new addresses.
    :type model: Addresses
    """

    def __init__(
        self, statements: AddressesStms, db_operations: Operations, model: Addresses
    ) -> None:
        """
        Initializes the CreateSrvc class with the provided statements, database operations, and model.

        :param statements: The SQL statements used for creating address data.
        :type statements: AddressesStms
        :param db_operations: The database operations object used for executing queries.
        :type db_operations: Operations
        :param model: The address model for creating new addresses.
        :type model: Addresses
        """
        self._statements: AddressesStms = statements
        self._db_ops: Operations = db_operations
        self._model: Addresses = model

    @property
    def statements(self) -> Addresses:
        """
        Returns the addresses SQL statements.

        :return: The addresses SQL statements.
        :rtype: AddressesStms
        """
        return self._statements

    @property
    def db_operations(self) -> Operations:
        """
        Returns the database operations object.

        :return: The database operations object.
        :rtype: Operations
        """
        return self._db_ops

    @property
    def model(self) -> Addresses:
        """
        Returns the address model.

        :return: The address model.
        :rtype: Addresses
        """
        return self._model

    async def create_address(
        self,
        parent_uuid: UUID4,
        address_data: AccountAddressesInternalCreate | EntityAddressesInternalCreate,
        db: AsyncSession,
    ) -> AddressesRes:
        """
        Creates a new address in the database.

        :param parent_uuid: The UUID of the parent (either an account or an entity).
        :type parent_uuid: UUID4
        :param address_data: The address data to be inserted.
        :type address_data: AccountAddressesCreate | EntityAddressesCreate
        :param db: The database session.
        :type db: AsyncSession
        :return: The created address.
        :rtype: AddressesRes
        :raises AddressExists: If the address already exists.
        :raises AddressNotExist: If the address creation failed.
        """
        addresses = self._model
        statement = self._statements.get_address_by_address(
            parent_uuid=parent_uuid,
            address_line1=address_data.address_line1,
            address_line2=address_data.address_line2,
            city=address_data.city,
        )
        address_exists: AddressesRes = await self._db_ops.return_one_row(
            service=cnst.ADDRESSES_CREATE_SERVICE, statement=statement, db=db
        )
        if not record_exists(instance=address_exists, exception=AddressExists):
            address: AddressesRes = await self._db_ops.add_instance(
                service=cnst.ADDRESSES_CREATE_SERVICE,
                model=addresses,
                data=address_data,
                db=db,
            )
            return record_not_exist(instance=address, exception=AddressNotExist)


class UpdateSrvc:
    """
    Service for updating addresses in the database.

    This class provides functionality to update existing address records in the database.

    :param statements: The SQL statements used for updating address data.
    :type statements: AddressesStms
    :param db_operations: The database operations object used for executing queries.
    :type db_operations: Operations
    """

    def __init__(self, statements: AddressesStms, db_operations: Operations) -> None:
        """
        Initializes the UpdateSrvc class with the provided statements and database operations.

        :param statements: The SQL statements used for updating address data.
        :type statements: AddressesStms
        :param db_operations: The database operations object used for executing queries.
        :type db_operations: Operations
        """
        self._statements: AddressesStms = statements
        self._db_ops: Operations = db_operations

    @property
    def statements(self) -> Addresses:
        """
        Returns the addresses SQL statements.

        :return: The addresses SQL statements.
        :rtype: AddressesStms
        """
        return self._statements

    @property
    def db_operations(self) -> Operations:
        """
        Returns the database operations object.

        :return: The database operations object.
        :rtype: Operations
        """
        return self._db_ops

    async def update_address(
        self,
        parent_uuid: UUID4,
        parent_table: Literal["entities", "accounts"],
        address_uuid: UUID4,
        address_data: AddressesUpdate,
        db: AsyncSession,
    ) -> AddressesRes:
        """
        Updates an existing address in the database.

        :param parent_uuid: The UUID of the parent (either an entity or an account).
        :type parent_uuid: UUID4
        :param parent_table: The table the address is associated with, either "entities" or "accounts".
        :type parent_table: Literal["entities", "accounts"]
        :param address_uuid: The UUID of the address to update.
        :type address_uuid: UUID4
        :param address_data: The new data to update the address with.
        :type address_data: AddressesUpdate
        :param db: The database session.
        :type db: AsyncSession
        :return: The updated address.
        :rtype: AddressesRes
        :raises AddressNotExist: If the address does not exist.
        """
        statement = self._statements.update_address(
            parent_uuid=parent_uuid,
            parent_table=parent_table,
            addresses_uuid=address_uuid,
            address_data=address_data,
        )
        address: AddressesRes = await self._db_ops.return_one_row(
            service=cnst.ADDRESSES_UPDATE_SERVICE, statement=statement, db=db
        )
        return record_not_exist(instance=address, exception=AddressNotExist)


class DelSrvc:
    """
    Service for deleting addresses in the database.

    This class provides functionality to perform soft deletion of addresses in the database.

    :param statements: The SQL statements used for deleting address data.
    :type statements: AddressesStms
    :param db_operations: The database operations object used for executing queries.
    :type db_operations: Operations
    """

    def __init__(self, statements: AddressesStms, db_operations: Operations) -> None:
        """
        Initializes the DelSrvc class with the provided statements and database operations.

        :param statements: The SQL statements used for deleting address data.
        :type statements: AddressesStms
        :param db_operations: The database operations object used for executing queries.
        :type db_operations: Operations
        """
        self._statements: AddressesStms = statements
        self._db_ops: Operations = db_operations

    @property
    def statements(self) -> Addresses:
        """
        Returns the addresses SQL statements.

        :return: The addresses SQL statements.
        :rtype: AddressesStms
        """
        return self._statements

    @property
    def db_operations(self) -> Operations:
        """
        Returns the database operations object.

        :return: The database operations object.
        :rtype: Operations
        """
        return self._db_ops

    async def soft_del_address(
        self,
        parent_uuid: UUID4,
        parent_table: Literal["entities", "accounts"],
        address_uuid: UUID4,
        address_data: AddressesDel,
        db: AsyncSession,
    ) -> AddressesDelRes:
        """
        Soft deletes an address in the database.

        :param parent_uuid: The UUID of the parent (either an entity or an account).
        :type parent_uuid: UUID4
        :param parent_table: The table the address is associated with, either "entities" or "accounts".
        :type parent_table: Literal["entities", "accounts"]
        :param address_uuid: The UUID of the address to delete.
        :type address_uuid: UUID4
        :param address_data: The data for performing the soft delete of the address.
        :type address_data: AddressesDel
        :param db: The database session.
        :type db: AsyncSession
        :return: The result of the soft delete operation.
        :rtype: AddressesDelRes
        :raises AddressNotExist: If the address does not exist.
        """
        statement = self._statements.update_address(
            parent_uuid=parent_uuid,
            parent_table=parent_table,
            addresses_uuid=address_uuid,
            address_data=address_data,
        )
        address: AddressesDelRes = await self._db_ops.return_one_row(
            service=cnst.ADDRESSES_DEL_SERVICE, statement=statement, db=db
        )
        return record_not_exist(instance=address, exception=AddressNotExist)
