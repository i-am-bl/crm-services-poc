from typing import List
from pydantic import UUID4
from sqlalchemy import Select, and_, func, update, values
from sqlalchemy.ext.asyncio import AsyncSession

from ..constants import constants as cnst
from ..database.operations import Operations
from ..exceptions import InvoiceExists, InvoiceNotExist
from ..models.invoices import Invoices
from ..schemas.invoices import (
    InvoicesInternalCreate,
    InvoicesInternalUpdate,
    InvoicesRes,
    InvoicesDel,
    InvoicesDelRes,
    InvoicesPgRes,
)
from ..statements.invoices import InvoicesStms
from ..utilities import pagination
from ..utilities.data import record_exists, record_not_exist


class ReadSrvc:
    """
    Service for reading invoice records from the database.

    This class provides functionality to fetch single or multiple invoices, count invoices,
    and return paginated invoices based on the provided parameters.

    :param statements: The SQL statements used for reading invoice records.
    :type statements: InvoicesStms
    :param db_operations: The database operations object used for executing queries.
    :type db_operations: Operations
    """

    def __init__(self, statements: InvoicesStms, db_operations: Operations) -> None:
        """
        Initializes the ReadSrvc class with the provided statements and database operations.

        :param statements: The SQL statements used for reading invoice records.
        :type statements: InvoicesStms
        :param db_operations: The database operations object used for executing queries.
        :type db_operations: Operations
        """
        self._statements: InvoicesStms = statements
        self._db_ops: Operations = db_operations

    @property
    def statements(self) -> InvoicesStms:
        """
        Returns the instance of InvoicesStms.

        :returns: The SQL statements for reading invoice records.
        :rtype: InvoicesStms
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

    async def get_invoice(self, invoice_uuid: UUID4, db: AsyncSession):
        """
        Retrieves a single invoice record by its UUID.

        :param invoice_uuid: The UUID of the invoice to be fetched.
        :type invoice_uuid: UUID4
        :param db: The asynchronous session for database operations.
        :type db: AsyncSession

        :returns: The invoice record if found, or an error if the invoice does not exist.
        :rtype: InvoicesRes
        """
        statement = self._statements.get_invoices(invoice_uuid=invoice_uuid)
        invoice = await self._db_ops.return_one_row(
            service=cnst.INVOICES_READ_SERV, statement=statement, db=db
        )
        return record_not_exist(instance=invoice, exception=InvoiceNotExist)

    async def get_invoices(
        self, limit: int, offset: int, db: AsyncSession
    ) -> InvoicesRes:
        """
        Retrieves a list of invoice records with pagination support.

        :param limit: The maximum number of invoices to retrieve.
        :type limit: int
        :param offset: The offset from which to start fetching invoices.
        :type offset: int
        :param db: The asynchronous session for database operations.
        :type db: AsyncSession

        :returns: A list of invoices if found, or an error if no invoices exist.
        :rtype: InvoicesRes
        """
        statement = self._statements.get_invoices(limit=limit, offset=offset)
        invoices: InvoicesRes = await self._db_ops.return_all_rows(
            service=cnst.INVOICES_READ_SERV, statement=statement, db=db
        )
        return record_not_exist(instance=invoices, exception=InvoiceNotExist)

    async def get_invoices_ct(self, db: AsyncSession) -> int:
        """
        Retrieves the total count of invoices in the database.

        :param db: The asynchronous session for database operations.
        :type db: AsyncSession

        :returns: The total count of invoices.
        :rtype: int
        """
        statement = self._statements.get_invoices_ct()
        return await self._db_ops.return_count(
            service=cnst.INVOICES_READ_SERV, statement=statement, db=db
        )

    async def paginated_invoices(
        self, page: int, limit: int, db: AsyncSession
    ) -> InvoicesPgRes:
        """
        Retrieves a paginated list of invoices based on the specified page and limit.

        :param page: The current page number.
        :type page: int
        :param limit: The number of invoices per page.
        :type limit: int
        :param db: The asynchronous session for database operations.
        :type db: AsyncSession

        :returns: A paginated result containing invoices and pagination metadata.
        :rtype: InvoicesPgRes
        """
        total_count: int = await self.get_invoices_ct(db=db)
        offset: int = pagination.page_offset(page=page, limit=limit)
        has_more: bool = pagination.has_more_items(
            total_count=total_count, page=page, limit=limit
        )
        invoices: List[InvoicesRes] = await self.get_invoices(
            limit=limit, offset=offset, db=db
        )
        return InvoicesPgRes(
            total=total_count,
            page=page,
            limit=limit,
            has_more=has_more,
            invoices=invoices,
        )


class CreateSrvc:
    """
    Service for creating invoice records in the database.

    This class provides functionality to create a new invoice record in the database.

    :param statements: The SQL statements used for interacting with invoices.
    :type statements: InvoicesStms
    :param db_operations: The database operations object used for executing queries.
    :type db_operations: Operations
    :param model: The model representing invoice records.
    :type model: Invoices
    """

    def __init__(
        self, statements: InvoicesStms, db_operations: Operations, model: Invoices
    ) -> None:
        """
        Initializes the CreateSrvc class with the provided statements, database operations, and model.

        :param statements: The SQL statements used for interacting with invoices.
        :type statements: InvoicesStms
        :param db_operations: The database operations object used for executing queries.
        :type db_operations: Operations
        :param model: The model representing invoice records.
        :type model: Invoices
        """
        self._statements: InvoicesStms = statements
        self._db_ops: Operations = db_operations
        self._model: Invoices = model

    @property
    def statements(self) -> InvoicesStms:
        """
        Returns the instance of InvoicesStms.

        :returns: The SQL statements for interacting with invoices.
        :rtype: InvoicesStms
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
    def model(self) -> Invoices:
        """
        Returns the instance of the Invoices model.

        :returns: The invoice model.
        :rtype: Invoices
        """
        return self._model

    async def create_invoice(
        self,
        invoice_data: InvoicesInternalCreate,
        db: AsyncSession,
    ) -> InvoicesRes:
        """
        Creates a new invoice record in the database.

        :param invoice_data: The data for creating the new invoice.
        :type invoice_data: InvoicesInternalCreate
        :param db: The asynchronous session for database operations.
        :type db: AsyncSession

        :returns: The created invoice record if successful, or an error if the invoice creation fails.
        :rtype: InvoicesRes
        """
        invoices = self._model
        statement = self._statements.get_invoices_by_order(
            order_uuid=invoice_data.order_uuid
        )
        invoice_exists: InvoicesRes = await self._db_ops.return_one_row(
            service=cnst.INVOICES_CREATE_SERV, statement=statement, db=db
        )
        record_exists(instance=invoice_exists, exception=InvoiceExists)
        invoice = await self._db_ops.add_instance(
            service=cnst.INVOICES_CREATE_SERV,
            model=invoices,
            data=invoice_data,
            db=db,
        )
        return record_not_exist(instance=invoice, exception=InvoiceNotExist)


class UpdateSrvc:
    """
    Service for updating invoice records in the database.

    This class provides functionality to update an existing invoice record in the database.

    :param statements: The SQL statements used for interacting with invoices.
    :type statements: InvoicesStms
    :param db_operations: The database operations object used for executing queries.
    :type db_operations: Operations
    """

    def __init__(self, statements: InvoicesStms, db_operations: Operations) -> None:
        """
        Initializes the UpdateSrvc class with the provided statements and database operations.

        :param statements: The SQL statements used for interacting with invoices.
        :type statements: InvoicesStms
        :param db_operations: The database operations object used for executing queries.
        :type db_operations: Operations
        """
        self._statements: InvoicesStms = statements
        self._db_ops: Operations = db_operations

    @property
    def statements(self) -> InvoicesStms:
        """
        Returns the instance of InvoicesStms.

        :returns: The SQL statements for interacting with invoices.
        :rtype: InvoicesStms
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

    async def update_invoice(
        self,
        invoice_uuid: UUID4,
        invoice_data: InvoicesInternalUpdate,
        db: AsyncSession,
    ) -> InvoicesRes:
        """
        Updates an existing invoice record in the database.

        :param invoice_uuid: The UUID of the invoice to be updated.
        :type invoice_uuid: UUID4
        :param invoice_data: The data to update the invoice.
        :type invoice_data: InvoicesInternalUpdate
        :param db: The asynchronous session for database operations.
        :type db: AsyncSession

        :returns: The updated invoice record if successful, or an error if the update fails.
        :rtype: InvoicesRes
        """
        statement = self._statements.update_invoices(
            invoice_uuid=invoice_uuid, invoice_data=invoice_data
        )
        invoice: InvoicesRes = await self._db_ops.return_one_row(
            service=cnst.INVOICES_UPDATE_SERV, statement=statement, db=db
        )
        return record_not_exist(instance=invoice, exception=InvoiceNotExist)


class DelSrvc:
    """
    Service for soft-deleting invoice records in the database.

    This class provides functionality to soft-delete an invoice record by updating its status in the database.

    :param statements: The SQL statements used for interacting with invoices.
    :type statements: InvoicesStms
    :param db_operations: The database operations object used for executing queries.
    :type db_operations: Operations
    """

    def __init__(self, statements: InvoicesStms, db_operations: Operations) -> None:
        """
        Initializes the DelSrvc class with the provided statements and database operations.

        :param statements: The SQL statements used for interacting with invoices.
        :type statements: InvoicesStms
        :param db_operations: The database operations object used for executing queries.
        :type db_operations: Operations
        """
        self._statements: InvoicesStms = statements
        self._db_ops: Operations = db_operations

    @property
    def statements(self) -> InvoicesStms:
        """
        Returns the instance of InvoicesStms.

        :returns: The SQL statements for interacting with invoices.
        :rtype: InvoicesStms
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

    async def soft_del_invoice(
        self,
        invoice_uuid: UUID4,
        invoice_data: InvoicesDel,
        db: AsyncSession,
    ) -> InvoicesDelRes:
        """
        Soft-deletes an existing invoice record by updating its status in the database.

        :param invoice_uuid: The UUID of the invoice to be soft-deleted.
        :type invoice_uuid: UUID4
        :param invoice_data: The data containing the soft delete status for the invoice.
        :type invoice_data: InvoicesDel
        :param db: The asynchronous session for database operations.
        :type db: AsyncSession

        :returns: The updated invoice record with the soft delete status if successful,
                 or an error if the invoice does not exist.
        :rtype: InvoicesDelRes
        """
        statement = self._statements.update_invoices(
            invoice_uuid=invoice_uuid, invoice_data=invoice_data
        )
        invoice: InvoicesDelRes = await self._db_ops.return_one_row(
            service=cnst.INVOICES_DEL_SERV, statement=statement, db=db
        )
        return record_not_exist(instance=invoice, exception=InvoiceNotExist)
