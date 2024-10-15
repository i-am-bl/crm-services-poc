from uuid import uuid4
from pydantic import UUID4
from models.sys_base import SysBase
from sqlalchemy import UUID, Integer, String, text
from sqlalchemy.orm import Mapped, mapped_column


class Addresses(SysBase):
    __tablename__ = "em_addresses"
    __table_args__ = {"schema": "sales"}

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, nullable=False
    )
    uuid: Mapped[uuid4] = mapped_column(
        UUID(as_uuid=True),
        unique=True,
        nullable=False,
        server_default=text("gen_random_uuid()"),
    )

    entity_id: Mapped[int] = mapped_column(Integer, nullable=False)
    entity_uuid: Mapped[uuid4] = mapped_column(UUID(as_uuid=True), nullable=False)

    address_line1: Mapped[str] = mapped_column(String(325), nullable=True)
    address_line2: Mapped[str] = mapped_column(String(325), nullable=True)
    city: Mapped[str] = mapped_column(String(325), nullable=True)
    county_cd: Mapped[str] = mapped_column(String(325), nullable=True)
    # state: Mapped[str] = mapped_column(String(325), nullable=True)
    # country: Mapped[str] = mapped_column(String(325), nullable=True)
    # zip: Mapped[str] = mapped_column(String(5), nullable=True)
    # zip_plus4: Mapped[str] = mapped_column(String(4), nullable=True)
