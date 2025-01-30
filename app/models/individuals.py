from uuid import UUID

from sqlalchemy import UUID, Integer, String, text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .sys_base import SysBase


class Individuals(SysBase):
    """
    This SQLAlchemy model represents an individual associated with an entity,
    storing personal details like the name and the entity they are linked to.

    ivars:
        id: The primary key of the individual.
        :vartype id: int
        uuid: Unique identifier for the individual, generated by the database.
        :vartype uuid: UUID
        entity_uuid: Foreign key referencing the associated entity.
        :vartype entity_uuid: UUID
        first_name: The first name of the individual.
        :vartype first_name: str
        last_name: The last name of the individual.
        :vartype last_name: str
        entity: Relationship to the `Entities` model.
        :vartype entity: Entities
    """

    __tablename__ = "em_individuals"
    __table_args__ = {"schema": "sales"}

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, nullable=False, autoincrement=True
    )
    uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), nullable=False, server_default=text("gen_random_uuid()")
    )

    entity_uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey(column="sales.em_entities.uuid"), nullable=False
    )

    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)

    # Parent relationship
    entity = relationship("Entities", back_populates="individual")
