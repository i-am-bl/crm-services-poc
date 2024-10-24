from datetime import date
from uuid import uuid4

from sqlalchemy import UUID, Date, Integer, String, text
from sqlalchemy.orm import Mapped, mapped_column

from .sys_base import SysBase


class ProductLists(SysBase):
    __tablename__ = "pm_product_lists"
    __table_args__ = {"schema": "sales"}

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, nullable=False, autoincrement=True
    )
    uuid: Mapped[uuid4] = mapped_column(
        UUID(as_uuid=True), nullable=False, server_default=text("gen_random_uuid()")
    )

    owner_uuid: Mapped[uuid4] = mapped_column(UUID(as_uuid=True), nullable=True)

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    start_on: Mapped[date] = mapped_column(Date, nullable=False)
    end_on: Mapped[date] = mapped_column(Date, nullable=False)
