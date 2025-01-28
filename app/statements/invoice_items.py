from pydantic import UUID4
from sqlalchemy import Select, Update, and_, func, update, values

from ..models.invoice_items import InvoiceItems
from ..utilities.utilities import DataUtils as di


class InvoiceItemsStms:
    def __init__(self, model: InvoiceItems) -> None:
        self._model: InvoiceItems = model

    @property
    def model(self) -> InvoiceItems:
        return self._model

    def get_invoice_items(self, invoice_uuid: UUID4, limit: int, offset: int) -> Select:
        invoice_items = self._model
        return (
            Select(invoice_items)
            .where(
                and_(
                    invoice_items.invoice_uuid == invoice_uuid,
                    invoice_items.sys_deleted_at == None,
                )
            )
            .offset(offset=offset)
            .limit(limit=limit)
        )

    def get_invoice_items_ct(self, invoice_uuid: UUID4) -> Select:
        invoice_items = self._model
        return (
            Select(func.count())
            .select_from(invoice_items)
            .where(
                and_(
                    invoice_items.invoice_uuid == invoice_uuid,
                    invoice_items.sys_deleted_at == None,
                )
            )
        )

    def get_invoice_item(self, invoice_uuid: UUID4, invoice_item_uuid: UUID4) -> Select:
        invoice_items = self._model
        return Select(invoice_items).where(
            and_(
                invoice_items.invoice_uuid == invoice_uuid,
                invoice_items.uuid == invoice_item_uuid,
                invoice_items.sys_deleted_at == None,
            )
        )

    def update_invoice_item(
        self, invoice_uuid: UUID4, invoice_item_uuid: UUID4, invoice_item_data: object
    ) -> Update:
        invoice_items = self._model
        return (
            update(invoice_items)
            .where(
                and_(
                    invoice_items.invoice_uuid == invoice_uuid,
                    invoice_items.uuid == invoice_item_uuid,
                    invoice_items.sys_deleted_at == None,
                )
            )
            .values(di.set_empty_strs_null(values=invoice_item_data))
            .returning(invoice_items)
        )
