from uuid import uuid4

from sqlalchemy import UUID, Integer, String, text
from sqlalchemy.orm import Mapped, mapped_column

from .sys_base import SysBase


class NonIndividuals(SysBase):
    __tablename__ = "em_non_individuals"
    __table_args__ = {"schema": "sales"}

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, nullable=False, autoincrement=True
    )
    uuid: Mapped[uuid4] = mapped_column(
        UUID(as_uuid=True), nullable=False, server_default=text("gen_random_uuid()")
    )

    entity_uuid: Mapped[uuid4] = mapped_column(UUID(as_uuid=True), nullable=False)

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    legal_name: Mapped[str] = mapped_column(String(100), nullable=True)
