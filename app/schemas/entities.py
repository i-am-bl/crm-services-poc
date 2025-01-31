from datetime import datetime
from typing import Annotated, List, Optional

from pydantic import UUID4, BaseModel, Field

from ..constants.enums import EntityTypes
from ._variables import TimeStamp
from .individuals import IndividualsDelRes, IndividualsRes
from .non_individuals import NonIndividualsDelRes, NonIndividualsRes


class Entities(BaseModel):
    """
    Base model representing an entity.
    """

    type: Annotated[EntityTypes, EntityTypes] = Field(
        ..., description="Type of entity (e.g., Individual, Organization)."
    )


class EntitiesCreate(Entities):
    """
    Model for creating a new entity record.
    """

    sys_created_at: datetime = Field(
        TimeStamp, description="Timestamp of when the entity was created."
    )
    sys_created_by: UUID4 = Field(
        ..., description="UUID of the user who created the entity."
    )


class EntitiesUpdate(Entities):
    """
    Model for updating an existing entity record.
    """

    sys_updated_at: datetime = Field(
        TimeStamp, description="Timestamp of when the entity was last updated."
    )
    sys_updated_by: Optional[UUID4] = Field(
        None, description="UUID of the user who last updated the entity."
    )


class EntitiesDel(BaseModel):
    """
    Model for marking an entity as deleted.
    """

    sys_deleted_at: datetime = Field(
        TimeStamp, description="Timestamp of when the entity was deleted."
    )
    sys_deleted_by: Optional[UUID4] = Field(
        None, description="UUID of the user who deleted the entity."
    )


class EntitiesRes(Entities):
    """
    Response model representing an entity.
    """

    id: int = Field(..., description="Unique identifier of the entity.")
    uuid: UUID4 = Field(..., description="UUID of the entity.")
    sys_created_at: datetime = Field(
        ..., description="Timestamp of when the entity was created."
    )
    sys_created_by: UUID4 = Field(
        ..., description="UUID of the user who created the entity."
    )
    sys_updated_at: Optional[datetime] = Field(
        None, description="Timestamp of when the entity was last updated."
    )
    sys_updated_by: Optional[UUID4] = Field(
        None, description="UUID of the user who last updated the entity."
    )

    class Config:
        from_attributes = True


class IndividualNonIndividualRes(BaseModel):
    """
    Model representing common fields for individuals and non-individuals.
    """

    entity_uuid: Optional[UUID4] = Field(
        None, description="UUID of the associated entity."
    )
    first_name: Optional[str] = Field(
        None, description="First name (if an individual)."
    )
    last_name: Optional[str] = Field(None, description="Last name (if an individual).")
    company_name: Optional[str] = Field(
        None, description="Company name (if a non-individual)."
    )

    class Config:
        from_attributes = True


class EntitiesIndividualRes(Entities):
    """
    Response model for an entity that is an individual.
    """

    id: int = Field(..., description="Unique identifier of the entity.")
    uuid: UUID4 = Field(..., description="UUID of the entity.")
    information: IndividualsRes = Field(
        ..., description="Detailed information about the individual."
    )
    sys_created_at: datetime = Field(
        ..., description="Timestamp of when the entity was created."
    )
    sys_created_by: UUID4 = Field(
        ..., description="UUID of the user who created the entity."
    )
    sys_updated_at: Optional[datetime] = Field(
        None, description="Timestamp of when the entity was last updated."
    )
    sys_updated_by: Optional[UUID4] = Field(
        None, description="UUID of the user who last updated the entity."
    )

    class Config:
        from_attributes = True


class EntitiesCombinedRes(BaseModel):
    """
    Response model combining entity, individual, and non-individual data.
    """

    entity: Optional[EntitiesRes] = Field(None, description="Entity response object.")
    individual: Optional[IndividualsRes] = Field(
        None, description="Individual response object (if applicable)."
    )
    non_individual: Optional[NonIndividualsRes] = Field(
        None, description="Non-individual response object (if applicable)."
    )


class EntitiesPgRes(BaseModel):
    """
    Paginated response model for entities.
    """

    total: int = Field(..., description="Total number of entity records available.")
    page: int = Field(..., description="Current page number.")
    limit: int = Field(..., description="Number of entity records per page.")
    has_more: bool = Field(
        ...,
        description="Indicates if there are more entity records beyond the current page.",
    )
    data: List[EntitiesRes] = Field(..., description="List of entity response objects.")


class EntitiesDelRes(EntitiesRes):
    """
    Response model for a deleted entity.
    """

    sys_deleted_at: datetime = Field(
        TimeStamp, description="Timestamp of when the entity was deleted."
    )
    sys_deleted_by: Optional[UUID4] = Field(
        None, description="UUID of the user who deleted the entity."
    )

    class Config:
        from_attributes = True


class EntitiesCombinedDelRes(BaseModel):
    """
    Response model combining deleted entity, individual, and non-individual data.
    """

    entity: Optional[EntitiesDelRes] = Field(
        None, description="Deleted entity response object."
    )
    individual: Optional[IndividualsDelRes] = Field(
        None, description="Deleted individual response object (if applicable)."
    )
    non_individual: Optional[NonIndividualsDelRes] = Field(
        None, description="Deleted non-individual response object (if applicable)."
    )
