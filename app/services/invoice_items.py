from typing import List

from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession


from ..constants import constants as cnst
from ..database.operations import Operations
from ..exceptions import InvoiceItemNotExist
from ..models.invoice_items import InvoiceItems
from ..schemas.invoice_items import (
    InvoiceItemsCreate,
    InvoiceItemsDel,
    InvoiceItemsDelRes,
    InvoiceItemsPgRes,
    InvoiceItemsRes,
    InvoiceItemsUpdate,
)
from ..statements.invoice_items import InvoiceItemsStms
from ..utilities import pagination
from ..utilities.utilities import DataUtils as di


class ReadService:
    def __init__(self, statements: InvoiceItemsStms, db_operations: Operations) -> None:
        self._statements: InvoiceItemsStms = statements
        self._db_ops: Operations = db_operations

    @property
    def statements(self) -> InvoiceItemsStms:
        return self._statements

    @property
    def db_operations(self) -> Operations:
        return self._db_ops

    async def get_invoice_item(
        self, invoice_uuid: UUID4, invoice_item_uuid: UUID4, db: AsyncSession, s
    ) -> InvoiceItemsRes:
        statement = self._statements.get_invoice_item(
            invoice_uuid=invoice_uuid, invoice_item_uuid=invoice_item_uuid
        )
        invoice_item: InvoiceItemsRes = await self._db_ops.return_one_row(
            service=cnst.INVOICE_ITEMS_READ_SERV, statement=statement, db=db
        )
        return di.record_not_exist(instance=invoice_item, exception=InvoiceItemNotExist)

    async def get_invoices_items(
        self,
        invoice_uuid: UUID4,
        limit: int,
        offset: int,
        db: AsyncSession,
    ) -> List[InvoiceItemsRes]:
        statement = self._statements.get_invoice_items(
            invoice_uuid=invoice_uuid, limit=limit, offset=offset
        )
        invoice_items: List[InvoiceItemsRes] = await self._db_ops.return_all_rows(
            cnst.INVOICE_ITEMS_READ_SERV, statement=statement, db=db
        )
        return di.record_not_exist(
            instance=invoice_items, exception=InvoiceItemNotExist
        )

    async def get_invoices_items_ct(
        self,
        invoice_uuid: UUID4,
        db: AsyncSession,
    ) -> int:
        statement = self._statements.get_invoice_items_ct(invoice_uuid=invoice_uuid)
        invoice_items = await self._db_ops.return_count(
            cnst.INVOICE_ITEMS_READ_SERV, statement=statement, db=db
        )
        return di.record_not_exist(model=invoice_items)

    async def paginated_invoice_items(
        self, invoice_uuid: UUID4, page: int, limit: int, db: AsyncSession
    ) -> InvoiceItemsPgRes:
        total_count = await self.get_invoices_items_ct(invoice_uuid=invoice_uuid, db=db)
        offset = pagination.page_offset(page=page, limit=limit)
        has_more = pagination.has_more_items(
            total_count=total_count, page=page, limit=limit
        )
        invoice_items: InvoiceItemsPgRes = await self.get_invoices_items(
            invoice_uuid=invoice_uuid, offset=offset, limit=limit, db=db
        )
        return InvoiceItemsPgRes(total=total_count)


class CreateService:
    def __init__(
        self,
        statements: InvoiceItemsStms,
        db_operations: Operations,
        model: InvoiceItems,
    ) -> None:
        self._statements: InvoiceItemsStms = statements
        self._db_ops: Operations = db_operations
        self._model: InvoiceItems = model

    @property
    def statements(self) -> InvoiceItemsStms:
        return self._statements

    @property
    def db_operations(self) -> Operations:
        return self._db_ops

    @property
    def model(self) -> InvoiceItems:
        return self._model

    async def create_invoice_item(
        self,
        invoice_uuid: UUID4,
        invoice_item_data: InvoiceItemsCreate,
        db: AsyncSession,
    ) -> InvoiceItemsRes:
        invoice_items = self._model
        invoice_item: InvoiceItemsRes = await self._db_ops.add_instances(
            service=cnst.INVOICE_ITEMS_CREATE_SERV,
            model=invoice_items,
            data=invoice_item_data,
            db=db,
        )
        return di.record_not_exist(instance=invoice_item, exception=InvoiceItemNotExist)


class UpdateService:
    def __init__(self, statements: InvoiceItemsStms, db_operations: Operations) -> None:
        self._statements: InvoiceItemsStms = statements
        self._db_ops: Operations = db_operations

    @property
    def statements(self) -> InvoiceItemsStms:
        return self._statements

    @property
    def db_operations(self) -> Operations:
        return self._db_ops

    async def update_invoice_item(
        self,
        invoice_uuid: UUID4,
        invoice_item_uuid: UUID4,
        invoice_item_data: InvoiceItemsUpdate,
        db: AsyncSession,
    ) -> InvoiceItemsRes:
        statement = self._statements.update_invoice_item(
            invoice_uuid=invoice_uuid,
            invoice_item_uuid=invoice_item_uuid,
            invoice_item_data=invoice_item_data,
        )
        invoice_item = await self._db_ops.return_one_row(
            cnst.INVOICE_ITEMS_UPDATE_SERV, statement=statement, db=db
        )
        return di.record_not_exist(instance=invoice_item, exception=InvoiceItemNotExist)


class DelService:
    def __init__(self, statements: InvoiceItemsStms, db_operations: Operations) -> None:
        self._statements: InvoiceItemsStms = statements
        self._db_ops: Operations = db_operations

    @property
    def statements(self) -> InvoiceItemsStms:
        return self._statements

    @property
    def db_operations(self) -> Operations:
        return self._db_ops

    async def soft_del_invoice_item(
        self,
        invoice_uuid: UUID4,
        invoice_item_uuid: UUID4,
        invoice_item_data: InvoiceItemsDel,
        db: AsyncSession,
    ) -> InvoiceItemsDelRes:
        statement = self._statements.update_invoice_item(
            invoice_uuid=invoice_uuid,
            invoice_item_uuid=invoice_item_uuid,
            invoice_item_data=invoice_item_data,
        )
        invoice_item: InvoiceItemsDelRes = await self._db_ops.return_one_row(
            cnst.INVOICE_ITEMS_DEL_SERV, statement=statement, db=db
        )
        return di.record_not_exist(instance=invoice_item, exception=InvoiceItemNotExist)
