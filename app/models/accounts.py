from datetime import date
from uuid import uuid4

from sqlalchemy import UUID, Date, Integer, String, text
from sqlalchemy.orm import Mapped, mapped_column

from .sys_base import SysBase


class Accounts(SysBase):
    __tablename__ = "acc_accounts"
    __table_args__ = {"schema": "sales"}

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, nullable=False, autoincrement=True
    )
    uuid: Mapped[uuid4] = mapped_column(
        UUID(as_uuid=True), nullable=False, server_default=text("gen_random_uuid()")
    )

    sys_value_status_uuid: Mapped[uuid4] = mapped_column(
        UUID(as_uuid=True), nullable=True
    )

    name: Mapped[str] = mapped_column(String(255), nullable=True)
    start_on: Mapped[date] = mapped_column(Date, nullable=True)
    end_on: Mapped[date] = mapped_column(Date, nullable=True)
