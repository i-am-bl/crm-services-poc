from uuid import uuid4

from sqlalchemy import UUID, Integer, text
from sqlalchemy.orm import Mapped, mapped_column

from .sys_base import SysBase

# TODO: create an api for this table or dicard it for now


class StatementItems(SysBase):
    __tablename__ = "om_statement_items"
    __table_args__ = {"schema": "sales"}

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, nullable=False, autoincrement=True
    )
    uuid: Mapped[uuid4] = mapped_column(
        UUID(as_uuid=True), nullable=False, server_default=text("gen_random_uuid()")
    )
    statement_id: Mapped[int] = mapped_column(Integer, nullable=False)
    statement_uuid: Mapped[uuid4] = mapped_column(UUID(as_uuid=True), nullable=False)
    invoice_items_id: Mapped[int] = mapped_column(Integer, nullable=False)
    invoice_items_uuid: Mapped[uuid4] = mapped_column(
        UUID(as_uuid=True), nullable=False
    )
