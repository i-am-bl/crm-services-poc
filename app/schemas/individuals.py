from datetime import datetime
from typing import List, Optional

from pydantic import UUID4, BaseModel, Field

from ._variables import ConstrainedStr, TimeStamp


class IndividualsCreate(BaseModel):
    """Represents an individual with basic personal information."""

    first_name: ConstrainedStr = Field(..., description="First name of the individual.")
    last_name: Optional[ConstrainedStr] = Field(
        None, description="Last name of the individual."
    )


class IndividualsInitCreate(IndividualsCreate):
    """Model for creating an individual entity."""

    entity_uuid: UUID4 = Field(
        ..., description="Unique identifier of the associated entity."
    )
    sys_created_at: datetime = Field(
        TimeStamp, description="Timestamp when the record was created."
    )
    sys_created_by: Optional[UUID4] = Field(
        None, description="UUID of the user who created the record."
    )


class IndividualsUpdate(BaseModel):
    """Model for updating an individual entity."""

    first_name: Optional[ConstrainedStr] = Field(
        None, description="Updated first name of the individual."
    )
    last_name: Optional[ConstrainedStr] = Field(
        None, description="Updated last name of the individual."
    )
    sys_updated_at: datetime = Field(
        TimeStamp, description="Timestamp when the record was last updated."
    )
    sys_updated_by: Optional[UUID4] = Field(
        None, description="UUID of the user who last updated the record."
    )


class IndividualsDel(BaseModel):
    """Model for deleting an individual entity."""

    sys_deleted_at: datetime = Field(
        TimeStamp, description="Timestamp when the record was deleted."
    )
    sys_deleted_by: Optional[UUID4] = Field(
        None, description="UUID of the user who deleted the record."
    )


class IndividualsRes(BaseModel):
    """Response model representing an individual entity."""

    uuid: UUID4 = Field(..., description="Unique identifier of the individual.")
    entity_uuid: UUID4 = Field(
        ..., description="Unique identifier of the associated entity."
    )
    first_name: Optional[ConstrainedStr] = Field(
        None, description="First name of the individual."
    )
    last_name: Optional[ConstrainedStr] = Field(
        None, description="Last name of the individual."
    )
    sys_created_at: datetime = Field(
        TimeStamp, description="Timestamp when the record was created."
    )
    sys_created_by: Optional[UUID4] = Field(
        None, description="UUID of the user who created the record."
    )
    sys_updated_at: Optional[datetime] = Field(
        None, description="Timestamp when the record was last updated."
    )
    sys_updated_by: Optional[UUID4] = Field(
        None, description="UUID of the user who last updated the record."
    )

    class Config:
        from_attributes = True


class IndividualsPgRes(BaseModel):
    """Paginated response model for individual entities."""

    total: int = Field(..., description="Total number of individual records.")
    page: int = Field(..., description="Current page number.")
    limit: int = Field(
        ..., description="Number of records per page."
    )  # Fixed typo from 'liimt' to 'limit'
    has_more: bool = Field(
        ..., description="Indicates if there are more records available."
    )
    individuals: Optional[List[IndividualsRes]] = Field(
        None, description="List of individual records."
    )


class IndividualsDelRes(IndividualsRes):
    """Response model for a deleted individual entity."""

    sys_deleted_at: datetime = Field(
        ..., description="Timestamp when the record was deleted."
    )
    sys_deleted_by: Optional[UUID4] = Field(
        None, description="UUID of the user who deleted the record."
    )

    class Config:
        from_attributes = True
