from datetime import datetime
from uuid import uuid4

from sqlalchemy import TIMESTAMP, UUID, String, text
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base

""" base table containing sys fields applicable to all tables """


class SysBase(Base):
    __tablename__ = "sys_base"
    __table_args__ = {"schema": "sales"}
    __abstract__ = True

    sys_created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    sys_created_by: Mapped[uuid4] = mapped_column(UUID(as_uuid=True), nullable=True)
    sys_updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=True
    )
    sys_updated_by: Mapped[uuid4] = mapped_column(UUID(as_uuid=True), nullable=True)
    sys_deleted_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=True
    )
    sys_deleted_by: Mapped[uuid4] = mapped_column(UUID(as_uuid=True), nullable=True)
