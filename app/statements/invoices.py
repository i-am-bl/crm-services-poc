from pydantic import UUID4
from sqlalchemy import Select, and_, func, update, values

from ..models.invoices import Invoices
from ..utilities.data import set_empty_strs_null


class InvoicesStms:
    """
    A class responsible for constructing SQLAlchemy queries and statements for managing invoice records.

    ivars:
    ivar: _model: Invoices: An instance of the Invoices model.
    """

    def __init__(self, model: Invoices) -> None:
        """
        Initializes the InvoicesStms class.

        :param model: Invoices: An instance of the Invoices model.
        :return: None
        """
        self._model: Invoices = model

    @property
    def model(self) -> Invoices:
        """
        Returns the Invoices model.

        :return: Invoices: The Invoices model instance.
        """
        return self._model

    def get_invoice(self, invoice_uuid: UUID4) -> Select:
        """
        Selects a specific invoice by its UUID.

        :param invoice_uuid: UUID4: The UUID of the invoice.
        :return: Select: A Select statement for the specific invoice.
        """
        invoices = self._model
        return Select(invoices).where(
            and_(invoices.uuid == invoice_uuid, invoices.sys_deleted_at == None)
        )

    def get_invoices_by_order(self, order_uuid: UUID4) -> Select:
        """
        Selects invoices associated with a specific order UUID.

        :param order_uuid: UUID4: The UUID of the order.
        :return: Select: A Select statement for invoices related to the order.
        """
        invoices = self._model
        return Select(invoices).where(
            and_(
                invoices.order_uuid == order_uuid,
                invoices.sys_deleted_at == None,
            )
        )

    def get_invoices(self, limit: int, offset: int) -> Select:
        """
        Selects invoices with pagination.

        :param limit: int: The maximum number of invoices to return.
        :param offset: int: The number of records to skip.
        :return: Select: A Select statement for invoices with pagination.
        """
        invoices = self._model
        return (
            Select(invoices)
            .where(invoices.sys_deleted_at == None)
            .offset(offset=offset)
            .limit(limit=limit)
        )

    def get_invoices_count(self) -> Select:
        """
        Selects the count of all invoices.

        :return: Select: A Select statement for the count of invoices.
        """
        invoices = self._model
        return (
            Select(func.count())
            .select_from(invoices)
            .where(invoices.sys_deleted_at == None)
        )

    def update_invoice(self, invoice_uuid: UUID4, invoice_data: object) -> Update:
        """
        Updates a specific invoice by its UUID.

        :param invoice_uuid: UUID4: The UUID of the invoice.
        :param invoice_data: object: The data to update the invoice with.
        :return: Update: An Update statement for the invoice.
        """
        invoices = self._model
        return (
            update(invoices)
            .where(and_(invoices.uuid == invoice_uuid, invoices.sys_deleted_at == None))
            .values(set_empty_strs_null(values=invoice_data))
            .returning(invoices)
        )
