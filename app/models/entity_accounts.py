from datetime import date
from uuid import uuid4

from sqlalchemy import UUID, Date, Integer, text
from sqlalchemy.orm import Mapped, mapped_column

from .sys_base import SysBase


class EntityAccounts(SysBase):
    __tablename__ = "em_entity_accounts"
    __table_args__ = {"schema": "sales"}
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    uuid: Mapped[uuid4] = mapped_column(
        UUID(as_uuid=True),
        nullable=False,
        server_default=text("gen_random_uuid()"),
        unique=True,
    )

    entity_id: Mapped[int] = mapped_column(Integer, nullable=False)
    entity_uuid: Mapped[uuid4] = mapped_column(UUID(as_uuid=True), nullable=False)
    account_id: Mapped[int] = mapped_column(Integer, nullable=False)
    account_uuid: Mapped[uuid4] = mapped_column(UUID(as_uuid=True), nullable=False)

    start_on: Mapped[date] = mapped_column(Date, nullable=True)
    end_on: Mapped[date] = mapped_column(Date, nullable=True)
