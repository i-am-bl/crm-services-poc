from datetime import datetime
from uuid import uuid4

from sqlalchemy import TIMESTAMP, UUID, Integer, String, text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.sys_base import SysBase


class SysUsers(SysBase):
    __tablename__ = "sys_users"
    __table_args__ = {"schema": "sales"}

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, nullable=False, autoincrement=True
    )
    uuid: Mapped[uuid4] = mapped_column(
        UUID(as_uuid=True),
        nullable=False,
        server_default=text("gen_random_uuid()"),
        unique=True,
    )

    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(325), nullable=False, unique=True)
    username: Mapped[str] = mapped_column(String(325), nullable=False)
    password: Mapped[str] = mapped_column(String(325), nullable=False)
    disabled_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=True
    )
