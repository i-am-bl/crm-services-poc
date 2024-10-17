from uuid import uuid4

from sqlalchemy import UUID, Integer, String, text
from sqlalchemy.orm import Mapped, mapped_column

from .sys_base import SysBase


class Numbers(SysBase):
    __tablename__ = "em_numbers"
    __table_args__ = {"schema": "sales"}

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, nullable=False, autoincrement=True
    )
    uuid: Mapped[uuid4] = mapped_column(
        UUID(as_uuid=True), nullable=False, server_default=text("gen_random_uuid()")
    )

    entity_id: Mapped[int] = mapped_column(Integer, nullable=False)
    entity_uuid: Mapped[uuid4] = mapped_column(UUID(as_uuid=True), nullable=False)
    # parent_table: Mapped[str] = mapped_column(String(100), nullable=False)
    sys_value_type_id: Mapped[int] = mapped_column(Integer, nullable=True)
    # TODO: change some of this to not be nullable

    country_code: Mapped[str] = mapped_column(String(1), nullable=True)
    area_code: Mapped[str] = mapped_column(String(3), nullable=True)
    line_number: Mapped[str] = mapped_column(String(4), nullable=True)
    extension: Mapped[str] = mapped_column(String(10), nullable=True)
