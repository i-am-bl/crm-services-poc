from uuid import uuid4

from sqlalchemy import UUID, CheckConstraint, Integer, String, text
from sqlalchemy.orm import Mapped, mapped_column

from .sys_base import SysBase


class Entities(SysBase):
    __tablename__ = "em_entities"
    __table_args__ = (
        CheckConstraint(
            "type in ('individual', 'non-individual')", name="entities_type_check"
        ),
        {"schema": "sales"},
    )

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, nullable=False, autoincrement=True
    )
    uuid: Mapped[uuid4] = mapped_column(
        UUID(as_uuid=True),
        nullable=False,
        server_default=text("gen_random_uuid()"),
        unique=True,
    )

    entity_types = ["individual", "non-individual"]
    type: Mapped[str] = mapped_column(String(50), nullable=False)
    tin: Mapped[str] = mapped_column(String(20), nullable=True)
