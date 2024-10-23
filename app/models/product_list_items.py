from decimal import Decimal
from uuid import uuid4

from sqlalchemy import UUID, Boolean, Integer, Numeric, text
from sqlalchemy.orm import Mapped, mapped_column

from .sys_base import SysBase


class ProductListItems(SysBase):
    __tablename__ = "pm_product_list_items"
    __table_args__ = {"schema": "sales"}

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, nullable=False, autoincrement=True
    )
    uuid: Mapped[uuid4] = mapped_column(
        UUID(as_uuid=True), nullable=False, server_default=text("gen_random_uuid()")
    )

    product_list_uuid: Mapped[uuid4] = mapped_column(UUID(as_uuid=True), nullable=False)
    product_uuid: Mapped[uuid4] = mapped_column(UUID(as_uuid=True), nullable=False)

    price: Mapped[Decimal] = mapped_column(
        Numeric(10, 2), nullable=False, server_default=text("0.00")
    )

    # local scope
    sys_allowed_price_increase: Mapped[bool] = mapped_column(
        Boolean, server_default=text("False"), nullable=False
    )
    man_allowed_price_increase: Mapped[bool] = mapped_column(
        Boolean, server_default=text("False"), nullable=False
    )
    sys_allowed_price_decrease: Mapped[bool] = mapped_column(
        Boolean, server_default=text("False"), nullable=False
    )
    man_allowed_price_decrease: Mapped[bool] = mapped_column(
        Boolean, server_default=text("False"), nullable=False
    )
