from typing import List
from pydantic import UUID4
from sqlalchemy import Select, and_, func, update, values
from sqlalchemy.ext.asyncio import AsyncSession

from ..constants import constants as cnst
from ..database.operations import Operations
from ..exceptions import InvoiceExists, InvoiceNotExist
from ..models.invoices import Invoices
from ..schemas.invoices import (
    InvoicesCreate,
    InvoicesUpdate,
    InvoicesRes,
    InvoicesDel,
    InvoicesDelRes,
    InvoicesPgRes,
)
from ..statements.invoices import InvoicesStms
from ..utilities import pagination
from ..utilities.utilities import DataUtils as di


class ReadSrvc:
    def __init__(self, statements: InvoicesStms, db_operations: Operations) -> None:
        self._statements: InvoicesStms = statements
        self._db_ops: Operations = db_operations

    @property
    def statements(self) -> InvoicesStms:
        return self._statements

    @property
    def db_operations(self) -> Operations:
        return self._db_ops

    async def get_invoice(self, invoice_uuid: UUID4, db: AsyncSession):
        statement = self._statements.get_invoices(invoice_uuid=invoice_uuid)
        invoice = await self._db_ops.return_one_row(
            service=cnst.INVOICES_READ_SERV, statement=statement, db=db
        )
        return di.record_not_exist(instance=invoice, exception=InvoiceNotExist)

    async def get_invoices(
        self, limit: int, offset: int, db: AsyncSession
    ) -> InvoicesRes:
        statement = self._statements.get_invoices(limit=limit, offset=offset)
        invoices: InvoicesRes = await self._db_ops.return_all_rows(
            service=cnst.INVOICES_READ_SERV, statement=statement, db=db
        )
        return di.record_not_exist(instance=invoices, exception=InvoiceNotExist)

    async def get_invoices_ct(self, db: AsyncSession) -> int:
        statement = self._statements.get_invoices_ct()
        return await self._db_ops.return_count(
            service=cnst.INVOICES_READ_SERV, statement=statement, db=db
        )

    async def paginated_invoices(
        self, page: int, limit: int, db: AsyncSession
    ) -> InvoicesPgRes:
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
    def __init__(
        self, statements: InvoicesStms, db_operations: Operations, model: Invoices
    ) -> None:
        self._statements: InvoicesStms = statements
        self._db_ops: Operations = db_operations
        self._model: Invoices = model

    @property
    def statements(self) -> InvoicesStms:
        return self._statements

    @property
    def db_operations(self) -> Operations:
        return self._db_ops

    @property
    def model(self) -> Invoices:
        return self._model

    async def create_invoice(
        self,
        invoice_data: InvoicesCreate,
        db: AsyncSession,
    ) -> InvoicesRes:
        invoices = self._model
        statement = self._statements.get_invoices_by_order(
            order_uuid=invoice_data.order_uuid
        )
        invoice_exists: InvoicesRes = await self._db_ops.return_one_row(
            service=cnst.INVOICES_CREATE_SERV, statement=statement, db=db
        )
        di.record_exists(instance=invoice_exists, exception=InvoiceExists)
        invoice = await self._db_ops.add_instance(
            service=cnst.INVOICES_CREATE_SERV,
            model=invoices,
            data=invoice_data,
            db=db,
        )
        return di.record_not_exist(instance=invoice, exception=InvoiceNotExist)


class UpdateSrvc:
    def __init__(self, statements: InvoicesStms, db_operations: Operations) -> None:
        self._statements: InvoicesStms = statements
        self._db_ops: Operations = db_operations

    @property
    def statements(self) -> InvoicesStms:
        return self._statements

    @property
    def db_operations(self) -> Operations:
        return self._db_ops

    async def update_invoice(
        self,
        invoice_uuid: UUID4,
        invoice_data: InvoicesUpdate,
        db: AsyncSession,
    ) -> InvoicesRes:
        statement = self._statements.update_invoices(
            invoice_uuid=invoice_uuid, invoice_data=invoice_data
        )
        invoice: InvoicesRes = await self._db_ops.return_one_row(
            service=cnst.INVOICES_UPDATE_SERV, statement=statement, db=db
        )
        return di.record_not_exist(instance=invoice, exception=InvoiceNotExist)


class DelSrvc:
    def __init__(self, statements: InvoicesStms, db_operations: Operations) -> None:
        self._statements: InvoicesStms = statements
        self._db_ops: Operations = db_operations

    @property
    def statements(self) -> InvoicesStms:
        return self._statements

    @property
    def db_operations(self) -> Operations:
        return self._db_ops

    async def soft_del_invoice(
        self,
        invoice_uuid: UUID4,
        invoice_data: InvoicesDel,
        db: AsyncSession,
    ) -> InvoicesDelRes:
        statement = self._statements.update_invoices(
            invoice_uuid=invoice_uuid, invoice_data=invoice_data
        )
        invoice: InvoicesDelRes = await self._db_ops.return_one_row(
            service=cnst.INVOICES_DEL_SERV, statement=statement, db=db
        )
        return di.record_not_exist(instance=invoice, exception=InvoiceNotExist)
