from decimal import Decimal
from uuid import uuid4

from sqlalchemy import UUID, CheckConstraint, Integer, Numeric, String, text
from sqlalchemy.orm import Mapped, mapped_column

from .sys_base import SysBase


class OrderItems(SysBase):
    __tablename__ = "om_order_items"
    __table_args__ = (
        CheckConstraint(
            "adjustment_type in ('dollar', 'percentage')",
            name="oder_items_adjustement_type",
        ),
        {"schema": "sales"},
    )
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, nullable=False, autoincrement=True
    )
    uuid: Mapped[uuid4] = mapped_column(
        UUID(as_uuid=True), nullable=False, server_default=text("gen_random_uuid()")
    )

    order_id: Mapped[int] = mapped_column(Integer, nullable=False)
    order_uuid: Mapped[uuid4] = mapped_column(UUID(as_uuid=True), nullable=False)
    product_list_item_id: Mapped[int] = mapped_column(Integer, nullable=False)
    product_list_item_uuid: Mapped[uuid4] = mapped_column(
        UUID(as_uuid=True), nullable=False
    )
    owner_id: Mapped[int] = mapped_column(Integer, nullable=True)
    adjusted_by_id: Mapped[int] = mapped_column(Integer, nullable=True)

    original_price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    adjustment_type: Mapped[str] = mapped_column(String(50), nullable=True)
    price_adjustment: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=True)