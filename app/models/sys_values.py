from uuid import uuid4

from sqlalchemy import UUID, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from .sys_base import SysBase


class SysValues(SysBase):
    """Key value pair reference data table"""

    __tablename__ = "sys_values"
    __table_args__ = {"schema": "sales"}

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, nullable=False, autoincrement=True
    )
    uuid: Mapped[uuid4] = mapped_column(UUID(as_uuid=True))
    table_name: Mapped[str] = mapped_column(String(100), nullable=True)
    name: Mapped[str] = mapped_column(String(100), nullable=True)
