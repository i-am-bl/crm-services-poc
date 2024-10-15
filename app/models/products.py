from uuid import uuid4

from sqlalchemy import UUID, Boolean, Integer, String, text
from sqlalchemy.orm import Mapped, mapped_column

from .sys_base import SysBase


class Products(SysBase):
    __tablename__ = "pm_products"
    __table_args__ = {"schema": "sales"}

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, nullable=False, autoincrement=True
    )
    uuid: Mapped[uuid4] = mapped_column(
        UUID(as_uuid=True), nullable=False, server_default=text("gen_random_uuid()")
    )

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    code: Mapped[str] = mapped_column(String(50), unique=True, nullable=True)
    terms: Mapped[str] = mapped_column(String(50), nullable=True)
    description: Mapped[str] = mapped_column(String(325), nullable=True)

    # global scope
    sys_allowed_price_increase: Mapped[bool] = mapped_column(
        Boolean, server_default=text("False"), nullable=False
    )
    sys_allowed_price_decrease: Mapped[bool] = mapped_column(
        Boolean, server_default=text("False"), nullable=False
    )
    man_allowed_price_increase: Mapped[bool] = mapped_column(
        Boolean, server_default=text("False"), nullable=False
    )
    man_allowed_price_decrease: Mapped[bool] = mapped_column(
        Boolean, server_default=text("False"), nullable=False
    )
