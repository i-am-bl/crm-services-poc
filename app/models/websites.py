from uuid import uuid4

from sqlalchemy import UUID, Integer, String, text
from sqlalchemy.orm import Mapped, mapped_column

from .sys_base import SysBase


class Websites(SysBase):
    __tablename__ = "em_websites"
    __table_args__ = {"schema": "sales"}

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, nullable=False, autoincrement=True
    )
    uuid: Mapped[uuid4] = mapped_column(
        UUID(as_uuid=True), nullable=False, server_default=text("gen_random_uuid()")
    )

    entity_uuid: Mapped[uuid4] = mapped_column(UUID(as_uuid=True), nullable=False)
    # parent_table: Mapped[str] = mapped_column(String(100), nullable=False)
    sys_value_type_uuid: Mapped[uuid4] = mapped_column(
        UUID(as_uuid=True), nullable=True
    )

    url: Mapped[str] = mapped_column(String(325), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=True)
