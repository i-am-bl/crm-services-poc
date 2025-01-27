from pydantic import UUID4
from sqlalchemy import Select, and_, func, update, values

from ..models.invoices import Invoices
from ..utilities.utilities import DataUtils as di


class InvoicesStms:
    def __init__(self, model: Invoices) -> None:
        self._model: Invoices = model

    @property
    def model(self) -> Invoices:
        return self._model

    def get_invoices(self, invoice_uuid: UUID4) -> Select:
        invoices = self._model
        return Select(invoices).where(
            and_(invoices.uuid == invoice_uuid, invoices.sys_deleted_at == None)
        )

    def get_invoices_by_order(self, order_uuid: UUID4):
        invoices = self._model
        return Select(invoices).where(
            and_(
                invoices.order_uuid == order_uuid,
                invoices.sys_deleted_at == None,
            )
        )

    def get_invoices(self, limit: int, offset: int):
        invoices = self._model
        return (
            Select(invoices)
            .where(invoices.sys_deleted_at == None)
            .offset(offset=offset)
            .limit(limit=limit)
        )

    def get_invoices_ct(
        self,
    ) -> Select:
        invoices = self._model
        return (
            Select(func.count())
            .select_from(invoices)
            .where(invoices.sys_deleted_at == None)
        )

    def update_invoices(self, invoice_uuid: UUID4, invoice_data: object) -> update:
        invoices = self._model
        return (
            update(invoices)
            .where(and_(invoices.uuid == invoice_uuid, invoices.sys_deleted_at == None))
            .values(di.set_empty_strs_null(values=invoice_data))
            .returning(invoices)
        )
