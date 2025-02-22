from decimal import Decimal
from uuid import UUID

from sqlalchemy import UUID, CheckConstraint, Integer, Numeric, String, text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .sys_base import SysBase


class InvoiceItems(SysBase):
    """
    This SQLAlchemy model represents an item within an invoice, linking to the respective
    product list item, order item, and invoice. It supports price adjustments and keeps
    a snapshot of the state for each invoice item.

    ivars:
        id: The primary key of the invoice item.
        :vartype id: int
        uuid: Unique identifier for the invoice item, generated by the database.
        :vartype uuid: UUID
        invoice_uuid: Foreign key linking the invoice item to a specific invoice.
        :vartype invoice_uuid: UUID
        order_item_uuid: Foreign key linking the invoice item to a specific order item.
        :vartype order_item_uuid: UUID
        product_list_item_uuid: Foreign key linking the invoice item to a specific product list item.
        :vartype product_list_item_uuid: UUID
        quantity: The quantity of the product in the invoice item.
        :vartype quantity: int
        owner_uuid: UUID representing the owner of the invoice item.
        :vartype owner_uuid: UUID, optional
        original_price: The original price of the product in the invoice item.
        :vartype original_price: Decimal
        adjustment_type: Type of adjustment for the price, either 'dollar' or 'percentage'.
        :vartype adjustment_type: str, optional
        price_adjustment: The amount of price adjustment applied to the product.
        :vartype price_adjustment: Decimal, optional
        invoice: Relationship to the `Invoices` model representing the invoice associated with the item.
        :vartype invoice: Invoices
        order_item: Relationship to the `OrderItems` model representing the order item associated with the invoice item.
        :vartype order_item: OrderItems
        product_list_item: Relationship to the `ProductListItems` model representing the product list item associated with the invoice item.
        :vartype product_list_item: ProductListItems
    """

    __tablename__ = "om_invoice_items"
    __table_args__ = (
        CheckConstraint(
            "adjustment_type in ('dollar', 'percentage')",
            name="inovice_items_adjustement_type",
        ),
        {"schema": "sales"},
    )
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, nullable=False, autoincrement=True
    )
    uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), nullable=False, server_default=text("gen_random_uuid()")
    )

    invoice_uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey(column="sales.om_invoices.uuid"), nullable=False
    )
    order_item_uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(column="sales.om_order_items.uuid"),
        nullable=False,
    )

    product_list_item_uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(column="sales.pm_product_list_items.uuid"),
        nullable=False,
    )
    quantity: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default=text("1")
    )
    owner_uuid: Mapped[UUID] = mapped_column(UUID(as_uuid=True), nullable=True)

    original_price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    adjustment_type: Mapped[str] = mapped_column(String(50), nullable=True)
    price_adjustment: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=True)

    # Parent relationships
    invoice = relationship("Invoices", back_populates="invoice_items")
    order_item = relationship("OrderItems", back_populates="invoice_items")
    product_list_item = relationship("ProductListItems", back_populates="invoice_items")
