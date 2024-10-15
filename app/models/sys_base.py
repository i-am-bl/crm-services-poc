from datetime import datetime

from sqlalchemy import TIMESTAMP, String, text
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
    sys_created_by: Mapped[str] = mapped_column(String(100), nullable=True)
    sys_updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=True
    )
    sys_updated_by: Mapped[str] = mapped_column(String(100), nullable=True)
    sys_deleted_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=True
    )
    sys_deleted_by: Mapped[str] = mapped_column(String(100), nullable=True)
