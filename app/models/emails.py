from uuid import uuid4

from sqlalchemy import UUID, Integer, String, text
from sqlalchemy.orm import Mapped, mapped_column

from .sys_base import SysBase


class Emails(SysBase):
    __tablename__ = "em_emails"
    __table_args__ = {"schema": "sales"}

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, nullable=False, autoincrement=True
    )
    uuid: Mapped[uuid4] = mapped_column(
        UUID(as_uuid=True), nullable=False, server_default=text("gen_random_uuid()")
    )

    entity_id: Mapped[int] = mapped_column(Integer, nullable=False)
    entity_uuid: Mapped[uuid4] = mapped_column(UUID(as_uuid=True), nullable=False)

    email: Mapped[str] = mapped_column(
        String(325),
        nullable=False,
    )
    username: Mapped[str] = mapped_column(String(325), nullable=True)
    domain: Mapped[str] = mapped_column(String(325), nullable=True)
