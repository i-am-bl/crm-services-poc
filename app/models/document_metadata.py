from uuid import uuid4

from sqlalchemy import UUID, CheckConstraint, Integer, String, text
from sqlalchemy.orm import Mapped, mapped_column

from .sys_base import SysBase


class DocumentMetadata(SysBase):
    # TODO: Marking this as abstract for v1 to exclude from build
    __abstract__ = True
    __tablename__ = "document_metadata"
    __table_args__ = (
        CheckConstraint(
            "parent_table in ('accounts', 'entities')",
            name="document_metadata_parent_table",
        ),
        {"schema": "sales"},
    )

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, nullable=False, autoincrement=True
    )
    uuid: Mapped[uuid4] = mapped_column(
        UUID(as_uuid=True), nullable=False, server_default=text("gen_random_uuid()")
    )

    pareent_id: Mapped[int] = mapped_column(Integer, nullable=True)
    parent_uuid: Mapped[uuid4] = mapped_column(UUID(as_uuid=True), nullable=True)
    parent_table: Mapped[str] = mapped_column(String(50), nullable=True)
    sys_value_type_uuid: Mapped[uuid4] = mapped_column(
        UUID(as_uuid=True), nullable=False
    )

    # allows for obtional storage using a document store
    object_uuid: Mapped[uuid4] = mapped_column(UUID(as_uuid=True), nullable=True)
    url: Mapped[str] = mapped_column(String(325), nullable=True)
