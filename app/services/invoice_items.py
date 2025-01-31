from typing import List

from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession


from ..constants import constants as cnst
from ..database.operations import Operations
from ..exceptions import InvoiceItemNotExist
from ..models.invoice_items import InvoiceItems
from ..schemas.invoice_items import (
    InvoiceItemsInternalCreate,
    InvoiceItemsDel,
    InvoiceItemsDelRes,
    InvoiceItemsPgRes,
    InvoiceItemsRes,
    InvoiceItemsUpdate,
)
from ..statements.invoice_items import InvoiceItemsStms
from ..utilities import pagination
from ..utilities.data import record_not_exist


class ReadSrvc:
    """
    Service for reading invoice items data from the database.

    This class provides functionality to retrieve individual invoice items, list all invoice items for an invoice,
    and retrieve count-related information about invoice items.

    :param statements: The SQL statements used for retrieving invoice item data.
    :type statements: InvoiceItemsStms
    :param db_operations: The database operations object used for executing queries.
    :type db_operations: Operations
    """

    def __init__(self, statements: InvoiceItemsStms, db_operations: Operations) -> None:
        """
        Initializes the ReadSrvc class with the provided statements and database operations.

        :param statements: The SQL statements used for retrieving invoice item data.
        :type statements: InvoiceItemsStms
        :param db_operations: The database operations object used for executing queries.
        :type db_operations: Operations
        """
        self._statements: InvoiceItemsStms = statements
        self._db_ops: Operations = db_operations

    @property
    def statements(self) -> InvoiceItemsStms:
        """
        Returns the instance of InvoiceItemsStms.

        :returns: The SQL statements for retrieving invoice item data.
        :rtype: InvoiceItemsStms
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

    async def get_invoice_item(
        self,
        invoice_uuid: UUID4,
        invoice_item_uuid: UUID4,
        db: AsyncSession,
    ) -> InvoiceItemsRes:
        """
        Retrieves a specific invoice item record by its invoice UUID and item UUID.

        :param invoice_uuid: The UUID of the invoice to which the item belongs.
        :type invoice_uuid: UUID4
        :param invoice_item_uuid: The UUID of the invoice item being retrieved.
        :type invoice_item_uuid: UUID4
        :param db: The asynchronous session for database operations.
        :type db: AsyncSession

        :returns: The invoice item record if found, or an error if the record does not exist.
        :rtype: InvoiceItemsRes
        """
        statement = self._statements.get_invoice_item(
            invoice_uuid=invoice_uuid, invoice_item_uuid=invoice_item_uuid
        )
        invoice_item: InvoiceItemsRes = await self._db_ops.return_one_row(
            service=cnst.INVOICE_ITEMS_READ_SERV, statement=statement, db=db
        )
        return record_not_exist(instance=invoice_item, exception=InvoiceItemNotExist)

    async def get_invoices_items(
        self,
        invoice_uuid: UUID4,
        limit: int,
        offset: int,
        db: AsyncSession,
    ) -> List[InvoiceItemsRes]:
        """
        Retrieves a list of invoice items for a given invoice UUID with pagination.

        :param invoice_uuid: The UUID of the invoice for which items are being retrieved.
        :type invoice_uuid: UUID4
        :param limit: The maximum number of items to retrieve.
        :type limit: int
        :param offset: The offset for pagination.
        :type offset: int
        :param db: The asynchronous session for database operations.
        :type db: AsyncSession

        :returns: A list of invoice items for the given invoice, or an error if no items are found.
        :rtype: List[InvoiceItemsRes]
        """
        statement = self._statements.get_invoice_items(
            invoice_uuid=invoice_uuid, limit=limit, offset=offset
        )
        invoice_items: List[InvoiceItemsRes] = await self._db_ops.return_all_rows(
            cnst.INVOICE_ITEMS_READ_SERV, statement=statement, db=db
        )
        return record_not_exist(instance=invoice_items, exception=InvoiceItemNotExist)

    async def get_invoices_items_ct(
        self,
        invoice_uuid: UUID4,
        db: AsyncSession,
    ) -> int:
        """
        Retrieves the count of invoice items for a given invoice UUID.

        :param invoice_uuid: The UUID of the invoice for which the item count is being retrieved.
        :type invoice_uuid: UUID4
        :param db: The asynchronous session for database operations.
        :type db: AsyncSession

        :returns: The count of invoice items for the given invoice, or an error if the count cannot be retrieved.
        :rtype: int
        """
        statement = self._statements.get_invoice_items_ct(invoice_uuid=invoice_uuid)
        invoice_items_count: int = await self._db_ops.return_count(
            cnst.INVOICE_ITEMS_READ_SERV, statement=statement, db=db
        )
        return record_not_exist(model=invoice_items_count)

    async def paginated_invoice_items(
        self,
        invoice_uuid: UUID4,
        page: int,
        limit: int,
        db: AsyncSession,
    ) -> InvoiceItemsPgRes:
        """
        Retrieves invoice items for a given invoice with pagination details, including the total count
        and whether there are more items to retrieve.

        :param invoice_uuid: The UUID of the invoice for which items are being retrieved.
        :type invoice_uuid: UUID4
        :param page: The page number for pagination.
        :type page: int
        :param limit: The maximum number of items to retrieve per page.
        :type limit: int
        :param db: The asynchronous session for database operations.
        :type db: AsyncSession

        :returns: A paginated response with invoice items, including total count and pagination status.
        :rtype: InvoiceItemsPgRes
        """
        total_count = await self.get_invoices_items_ct(invoice_uuid=invoice_uuid, db=db)
        offset = pagination.page_offset(page=page, limit=limit)
        has_more = pagination.has_more_items(
            total_count=total_count, page=page, limit=limit
        )
        invoice_items: InvoiceItemsPgRes = await self.get_invoices_items(
            invoice_uuid=invoice_uuid, offset=offset, limit=limit, db=db
        )
        return InvoiceItemsPgRes(
            total=total_count, items=invoice_items, has_more=has_more
        )


class CreateSrvc:
    """
    Service for creating invoice item records in the database.

    This class provides functionality to create a new invoice item record.

    :param statements: The SQL statements used for creating invoice items.
    :type statements: InvoiceItemsStms
    :param db_operations: The database operations object used for executing queries.
    :type db_operations: Operations
    :param model: The model representing the invoice item.
    :type model: InvoiceItems
    """

    def __init__(
        self,
        statements: InvoiceItemsStms,
        db_operations: Operations,
        model: InvoiceItems,
    ) -> None:
        """
        Initializes the CreateSrvc class with the provided statements, database operations, and model.

        :param statements: The SQL statements used for creating invoice items.
        :type statements: InvoiceItemsStms
        :param db_operations: The database operations object used for executing queries.
        :type db_operations: Operations
        :param model: The model representing the invoice item.
        :type model: InvoiceItems
        """
        self._statements: InvoiceItemsStms = statements
        self._db_ops: Operations = db_operations
        self._model: InvoiceItems = model

    @property
    def statements(self) -> InvoiceItemsStms:
        """
        Returns the instance of InvoiceItemsStms.

        :returns: The SQL statements for creating invoice items.
        :rtype: InvoiceItemsStms
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
    def model(self) -> InvoiceItems:
        """
        Returns the model for invoice items.

        :returns: The model used for creating invoice item records.
        :rtype: InvoiceItems
        """
        return self._model

    async def create_invoice_item(
        self,
        invoice_uuid: UUID4,
        invoice_item_data: InvoiceItemsInternalCreate,
        db: AsyncSession,
    ) -> InvoiceItemsRes:
        """
        Creates a new invoice item record in the database.

        :param invoice_uuid: The UUID of the invoice to which the item belongs.
        :type invoice_uuid: UUID4
        :param invoice_item_data: The data for creating the invoice item.
        :type invoice_item_data: InvoiceItemsInternalCreate
        :param db: The asynchronous session for database operations.
        :type db: AsyncSession

        :returns: The created invoice item record if successful, or an error if creation fails.
        :rtype: InvoiceItemsRes
        """
        invoice_items = self._model
        invoice_item: InvoiceItemsRes = await self._db_ops.add_instances(
            service=cnst.INVOICE_ITEMS_CREATE_SERV,
            model=invoice_items,
            data=invoice_item_data,
            db=db,
        )
        return record_not_exist(instance=invoice_item, exception=InvoiceItemNotExist)


class UpdateSrvc:
    """
    Service for updating invoice item records in the database.

    This class provides functionality to update an existing invoice item record.

    :param statements: The SQL statements used for updating invoice items.
    :type statements: InvoiceItemsStms
    :param db_operations: The database operations object used for executing queries.
    :type db_operations: Operations
    """

    def __init__(self, statements: InvoiceItemsStms, db_operations: Operations) -> None:
        """
        Initializes the UpdateSrvc class with the provided statements and database operations.

        :param statements: The SQL statements used for updating invoice items.
        :type statements: InvoiceItemsStms
        :param db_operations: The database operations object used for executing queries.
        :type db_operations: Operations
        """
        self._statements: InvoiceItemsStms = statements
        self._db_ops: Operations = db_operations

    @property
    def statements(self) -> InvoiceItemsStms:
        """
        Returns the instance of InvoiceItemsStms.

        :returns: The SQL statements for updating invoice items.
        :rtype: InvoiceItemsStms
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

    async def update_invoice_item(
        self,
        invoice_uuid: UUID4,
        invoice_item_uuid: UUID4,
        invoice_item_data: InvoiceItemsUpdate,
        db: AsyncSession,
    ) -> InvoiceItemsRes:
        """
        Updates an existing invoice item record in the database.

        :param invoice_uuid: The UUID of the invoice to which the item belongs.
        :type invoice_uuid: UUID4
        :param invoice_item_uuid: The UUID of the invoice item to be updated.
        :type invoice_item_uuid: UUID4
        :param invoice_item_data: The data for updating the invoice item.
        :type invoice_item_data: InvoiceItemsUpdate
        :param db: The asynchronous session for database operations.
        :type db: AsyncSession

        :returns: The updated invoice item record if successful, or an error if the item is not found.
        :rtype: InvoiceItemsRes
        """
        statement = self._statements.update_invoice_item(
            invoice_uuid=invoice_uuid,
            invoice_item_uuid=invoice_item_uuid,
            invoice_item_data=invoice_item_data,
        )
        invoice_item = await self._db_ops.return_one_row(
            cnst.INVOICE_ITEMS_UPDATE_SERV, statement=statement, db=db
        )
        return record_not_exist(instance=invoice_item, exception=InvoiceItemNotExist)


class DelSrvc:
    """
    Service for deleting invoice item records in the database.

    This class provides functionality to soft delete invoice item records.

    :param statements: The SQL statements used for deleting invoice items.
    :type statements: InvoiceItemsStms
    :param db_operations: The database operations object used for executing queries.
    :type db_operations: Operations
    """

    def __init__(self, statements: InvoiceItemsStms, db_operations: Operations) -> None:
        """
        Initializes the DelSrvc class with the provided statements and database operations.

        :param statements: The SQL statements used for deleting invoice items.
        :type statements: InvoiceItemsStms
        :param db_operations: The database operations object used for executing queries.
        :type db_operations: Operations
        """
        self._statements: InvoiceItemsStms = statements
        self._db_ops: Operations = db_operations

    @property
    def statements(self) -> InvoiceItemsStms:
        """
        Returns the instance of InvoiceItemsStms.

        :returns: The SQL statements for deleting invoice items.
        :rtype: InvoiceItemsStms
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

    async def soft_del_invoice_item(
        self,
        invoice_uuid: UUID4,
        invoice_item_uuid: UUID4,
        invoice_item_data: InvoiceItemsDel,
        db: AsyncSession,
    ) -> InvoiceItemsDelRes:
        """
        Soft deletes an invoice item record in the database by updating its status.

        :param invoice_uuid: The UUID of the invoice to which the item belongs.
        :type invoice_uuid: UUID4
        :param invoice_item_uuid: The UUID of the invoice item to be deleted.
        :type invoice_item_uuid: UUID4
        :param invoice_item_data: The data for deleting the invoice item.
        :type invoice_item_data: InvoiceItemsDel
        :param db: The asynchronous session for database operations.
        :type db: AsyncSession

        :returns: The soft-deleted invoice item record if successful, or an error if the item is not found.
        :rtype: InvoiceItemsDelRes
        """
        statement = self._statements.update_invoice_item(
            invoice_uuid=invoice_uuid,
            invoice_item_uuid=invoice_item_uuid,
            invoice_item_data=invoice_item_data,
        )
        invoice_item: InvoiceItemsDelRes = await self._db_ops.return_one_row(
            cnst.INVOICE_ITEMS_DEL_SERV, statement=statement, db=db
        )
        return record_not_exist(instance=invoice_item, exception=InvoiceItemNotExist)
