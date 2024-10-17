from datetime import date
from uuid import uuid4

from sqlalchemy import UUID, Date, Integer, String, text
from sqlalchemy.orm import Mapped, mapped_column

from .sys_base import SysBase


class AcccountContracts(SysBase):
    __tablename__ = "acc_account_contracts"
    __table_args__ = {"schema": "sales"}

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, nullable=False, autoincrement=True
    )
    uuid: Mapped[uuid4] = mapped_column(
        UUID(as_uuid=True), nullable=False, server_default=text("gen_random_uuid()")
    )

    account_uuid: Mapped[uuid4] = mapped_column(UUID(as_uuid=True), nullable=False)
    document_metadata_id: Mapped[int] = mapped_column(Integer, nullable=True)
    document_metadata_uuid: Mapped[uuid4] = mapped_column(
        UUID(as_uuid=True), nullable=True
    )
    sys_value_type_id: Mapped[int] = mapped_column(Integer, nullable=True)

    start_on: Mapped[date] = mapped_column(Date, nullable=True)
    end_on: Mapped[date] = mapped_column(Date, nullable=True)
    notification_days: Mapped[int] = mapped_column(Integer, nullable=True)
    status: Mapped[str] = mapped_column(String(100), nullable=True)
