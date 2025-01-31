from pydantic import UUID4
from sqlalchemy import Select, Update, and_, func, update, values

from ..models.invoice_items import InvoiceItems
from ..utilities.data import set_empty_strs_null


class InvoiceItemsStms:
    """
    A class responsible for constructing SQLAlchemy queries and statements for managing invoice item records.

    ivars:
    ivar: _model: InvoiceItems: An instance of the InvoiceItems model.
    """

    def __init__(self, model: InvoiceItems) -> None:
        """
        Initializes the InvoiceItemsStms class.

        :param model: InvoiceItems: An instance of the InvoiceItems model.
        :return: None
        """
        self._model: InvoiceItems = model

    @property
    def model(self) -> InvoiceItems:
        """
        Returns the InvoiceItems model.

        :return: InvoiceItems: The InvoiceItems model instance.
        """
        return self._model

    def get_invoice_items(self, invoice_uuid: UUID4, limit: int, offset: int) -> Select:
        """
        Selects invoice items for a given invoice UUID with pagination.

        :param invoice_uuid: UUID4: The UUID of the invoice.
        :param limit: int: The maximum number of invoice items to return.
        :param offset: int: The number of records to skip.
        :return: Select: A Select statement for the invoice items.
        """
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
        """
        Selects the count of invoice items for a given invoice UUID.

        :param invoice_uuid: UUID4: The UUID of the invoice.
        :return: Select: A Select statement for the count of invoice items.
        """
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
        """
        Selects a specific invoice item by its invoice UUID and item UUID.

        :param invoice_uuid: UUID4: The UUID of the invoice.
        :param invoice_item_uuid: UUID4: The UUID of the invoice item.
        :return: Select: A Select statement for the specific invoice item.
        """
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
        """
        Updates an invoice item by invoice UUID and item UUID.

        :param invoice_uuid: UUID4: The UUID of the invoice.
        :param invoice_item_uuid: UUID4: The UUID of the invoice item.
        :param invoice_item_data: object: The data to update the invoice item with.
        :return: Update: An Update statement for the invoice item.
        """
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
            .values(set_empty_strs_null(values=invoice_item_data))
            .returning(invoice_items)
        )
