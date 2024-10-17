from uuid import uuid4

from sqlalchemy import UUID, Date, Integer, text
from sqlalchemy.orm import Mapped, mapped_column

from .sys_base import SysBase


class Invoices(SysBase):
    __tablename__ = "om_invoices"
    __table_args__ = {"schema": "sales"}

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, nullable=False, autoincrement=True
    )
    uuid: Mapped[uuid4] = mapped_column(
        UUID(as_uuid=True), nullable=False, server_default=text("gen_random_uuid()")
    )

    order_uuid: Mapped[uuid4] = mapped_column(UUID(as_uuid=True), nullable=False)
    sys_value_status_id: Mapped[int] = mapped_column(Integer, nullable=False)

    transacted_on: Mapped[Date] = mapped_column(Date, nullable=True)
    posted_on: Mapped[Date] = mapped_column(Date, nullable=True)
    paid_on: Mapped[Date] = mapped_column(Date, nullable=True)
