from datetime import datetime
from typing import Optional

from pydantic import UUID4, BaseModel, Field

from ._variables import ConstrainedStr, TimeStamp


class NonIndividualsCreate(BaseModel):
    """Represents a non-individual entity, such as a business or organization."""

    name: ConstrainedStr = Field(
        ..., description="Display name of the non-individual entity."
    )
    legal_name: Optional[ConstrainedStr] = Field(
        None, description="Legal registered name of the entity."
    )


class NonIndividualsInitCreate(NonIndividualsCreate):
    """Model for creating a non-individual entity."""

    entity_uuid: UUID4 = Field(..., description="UUID of the associated entity.")
    sys_created_by: Optional[UUID4] = Field(
        None, description="UUID of the user who created the entity."
    )
    sys_created_at: datetime = Field(
        TimeStamp, description="Timestamp when the entity was created."
    )


class NonIndividualsUpdate(BaseModel):
    """Model for updating a non-individual entity."""

    name: Optional[ConstrainedStr] = Field(
        None, description="Updated name of the entity."
    )
    legal_name: Optional[ConstrainedStr] = Field(
        None, description="Updated legal name of the entity."
    )


class NonIndividualsInternalUpdate(NonIndividualsUpdate):
    """Model for updating a non-individual entity.

    Hiding system level fields from the client.
    """

    sys_updated_at: datetime = Field(
        TimeStamp, description="Timestamp when the entity was last updated."
    )
    sys_updated_by: Optional[UUID4] = Field(
        None, description="UUID of the user who last updated the entity."
    )


class NonIndividualsDel(BaseModel):
    """Model for marking a non-individual entity as deleted."""

    sys_deleted_at: datetime = Field(
        TimeStamp, description="Timestamp when the entity was deleted."
    )
    sys_deleted_by: Optional[UUID4] = Field(
        None, description="UUID of the user who deleted the entity."
    )


class NonIndividualsRes(BaseModel):
    """Response model for a non-individual entity."""

    uuid: UUID4 = Field(
        ..., description="Unique identifier for the non-individual entity."
    )
    name: ConstrainedStr = Field(
        ..., description="Display name of the non-individual entity."
    )
    legal_name: Optional[ConstrainedStr] = Field(
        None, description="Legal registered name of the entity."
    )
    sys_created_at: datetime = Field(
        ..., description="Timestamp when the entity was created."
    )
    sys_created_by: Optional[UUID4] = Field(
        None, description="UUID of the user who created the entity."
    )
    sys_updated_at: Optional[datetime] = Field(
        None, description="Timestamp when the entity was last updated."
    )
    sys_updated_by: Optional[UUID4] = Field(
        None, description="UUID of the user who last updated the entity."
    )

    class Config:
        from_attributes = True


class NonIndividualsDelRes(NonIndividualsRes):
    """Response model for a deleted non-individual entity."""

    sys_deleted_at: datetime = Field(
        ..., description="Timestamp when the entity was deleted."
    )
    sys_deleted_by: Optional[UUID4] = Field(
        None, description="UUID of the user who deleted the entity."
    )

    class Config:
        from_attributes = True
