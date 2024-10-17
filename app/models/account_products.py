from datetime import date
from uuid import uuid4

from sqlalchemy import UUID, Date, Integer, text
from sqlalchemy.orm import Mapped, mapped_column

from .sys_base import SysBase


class AccountProducts(SysBase):
    __tablename__ = "acc_account_products"
    __table_args__ = {"schema": "sales"}

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, nullable=False, autoincrement=True
    )
    uuid: Mapped[uuid4] = mapped_column(
        UUID(as_uuid=True), nullable=False, server_default=text("gen_random_uuid()")
    )

    account_id: Mapped[int] = mapped_column(Integer, nullable=False)
    account_uuid: Mapped[uuid4] = mapped_column(UUID(as_uuid=True), nullable=False)
    product_id: Mapped[int] = mapped_column(Integer, nullable=False)
    product_uuid: Mapped[uuid4] = mapped_column(UUID(as_uuid=True), nullable=False)

    start_on: Mapped[date] = mapped_column(Date, nullable=False)
    end_on: Mapped[date] = mapped_column(Date, nullable=False)
