from uuid import uuid4

from sqlalchemy import UUID, Integer, String, text
from sqlalchemy.orm import Mapped, mapped_column

from .sys_base import SysBase


class Contacts(SysBase):
    # TODO: Marking this as abstract until finished, excluding for v1
    __abstract__ = True
    __tablename__ = "em_contacts"
    __table_args__ = {"schema": "sales"}

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, nullable=False, autoincrement=True
    )
    uuid: Mapped[uuid4] = mapped_column(
        UUID(as_uuid=True), nullable=False, server_default=text("gen_random_uuid()")
    )

    parent_table: Mapped[str] = mapped_column(String(50), nullable=True)
    parent_uuid: Mapped[uuid4] = mapped_column(UUID(as_uuid=True), nullable=False)
    child_table: Mapped[str] = mapped_column(String(50), nullable=True)
    child_uuid: Mapped[uuid4] = mapped_column(UUID(as_uuid=True), nullable=False)

    sys_value_type_uuid: Mapped[uuid4] = mapped_column(
        UUID(as_uuid=True), nullable=True
    )
