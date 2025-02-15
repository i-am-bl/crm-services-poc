from turtle import back
from uuid import UUID

from sqlalchemy import UUID, CheckConstraint, Integer, String, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .sys_base import SysBase


class Entities(SysBase):
    """
    Represents an entity in the system, which could be either an individual or a non-individual.
    This class captures the entity's unique identifier, type, and tax identification number (TIN),
    and establishes relationships with various models that store additional entity-related information.

    ivars:
        id: The primary key of the entity record.
        :vartype id: int
        uuid: Unique identifier for the entity, automatically generated by the database.
        :vartype uuid: UUID
        type: The type of the entity, either "individual" or "non-individual".
        :vartype type: str
        tin: The Tax Identification Number (TIN) associated with the entity (optional).
        :vartype tin: str, optional
        emails: Relationship to the `Emails` model, representing the email addresses associated with the entity.
        :vartype emails: list of Emails
        entity_accounts: Relationship to the `EntityAccounts` model, representing the accounts linked to the entity.
        :vartype entity_accounts: list of EntityAccounts
        individual: Relationship to the `Individuals` model, representing additional details for an individual entity.
        :vartype individual: Individuals
        non_individual: Relationship to the `NonIndividuals` model, representing additional details for a non-individual entity.
        :vartype non_individual: NonIndividuals
        numbers: Relationship to the `Numbers` model, representing phone numbers or other contact numbers associated with the entity.
        :vartype numbers: list of Numbers
        websites: Relationship to the `Websites` model, representing the websites associated with the entity.
        :vartype websites: list of Websites
    """

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
    uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        nullable=False,
        server_default=text("gen_random_uuid()"),
        unique=True,
    )

    entity_types = ["individual", "non-individual"]
    type: Mapped[str] = mapped_column(String(50), nullable=False)
    tin: Mapped[str] = mapped_column(String(20), nullable=True)

    # Child relationships
    emails = relationship("Emails", back_populates="entity")
    entity_accounts = relationship("EntityAccounts", back_populates="entity")
    individual = relationship("Individuals", back_populates="entity")
    non_individual = relationship("NonIndividuals", back_populates="entity")
    numbers = relationship("Numbers", back_populates="entity")
    websites = relationship("Websites", back_populates="entity")
