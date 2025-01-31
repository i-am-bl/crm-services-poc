from datetime import datetime
from typing import List, Optional

from pydantic import UUID4, BaseModel, Field

from ._variables import ConstrainedStr, TimeStamp


class NumbersCreate(BaseModel):
    """Represents a structured phone number with country code, area code, and line number."""

    entity_uuid: UUID4 = Field(..., description="UUID of the associated entity.")
    country_code: Optional[ConstrainedStr] = Field(
        None, min_length=1, max_length=1, description="Single-character country code."
    )
    area_code: Optional[ConstrainedStr] = Field(
        None, min_length=3, max_length=3, description="Three-digit area code."
    )
    line_number: Optional[ConstrainedStr] = Field(
        None, min_length=4, max_length=4, description="Four-digit line number."
    )
    extension: Optional[ConstrainedStr] = Field(
        None, description="Optional phone number extension."
    )


class NumbersInternalCreate(NumbersCreate):
    """Model for creating a new phone number entry."""

    sys_created_at: datetime = Field(
        TimeStamp, description="Timestamp when the entry was created."
    )
    sys_created_by: Optional[UUID4] = Field(
        None, description="UUID of the user who created the entry."
    )


class NumbersUpdate(BaseModel):
    """Model for updating an existing phone number entry."""

    country_code: Optional[ConstrainedStr] = Field(
        None,
        min_length=1,
        max_length=1,
        description="Updated single-character country code.",
    )
    area_code: Optional[ConstrainedStr] = Field(
        None, min_length=3, max_length=3, description="Updated three-digit area code."
    )
    line_number: Optional[ConstrainedStr] = Field(
        None, min_length=4, max_length=4, description="Updated four-digit line number."
    )
    extension: Optional[ConstrainedStr] = Field(
        None, description="Updated phone number extension."
    )


class NumbersInternalUpdate(NumbersUpdate):
    """Model for updating an existing phone number entry.

    Hiding system level fields from client.
    """

    sys_updated_at: datetime = Field(
        TimeStamp, description="Timestamp when the entry was last updated."
    )
    sys_updated_by: Optional[UUID4] = Field(
        None, description="UUID of the user who last updated the entry."
    )


class NumbersDel(BaseModel):
    """Model for marking a phone number entry as deleted."""

    sys_deleted_at: datetime = Field(
        TimeStamp, description="Timestamp when the entry was deleted."
    )
    sys_deleted_by: Optional[UUID4] = Field(
        None, description="UUID of the user who deleted the entry."
    )


class NumbersRes(BaseModel):
    """Response model for a phone number entry."""

    id: int = Field(..., description="Database identifier for the phone number entry.")
    uuid: UUID4 = Field(
        ..., description="Unique identifier for the phone number entry."
    )
    entity_uuid: UUID4 = Field(..., description="UUID of the associated entity.")
    country_code: Optional[str] = Field(
        None, description="Single-character country code."
    )
    area_code: Optional[str] = Field(None, description="Three-digit area code.")
    line_number: Optional[str] = Field(None, description="Four-digit line number.")
    extension: Optional[str] = Field(
        None, description="Optional phone number extension."
    )

    class Config:
        from_attributes = True


class NumbersPgRes(BaseModel):
    """Paginated response model for phone number entries."""

    total: int = Field(..., description="Total number of phone number entries.")
    page: int = Field(..., description="Current page number.")
    limit: int = Field(..., description="Maximum number of entries per page.")
    has_more: bool = Field(
        ..., description="Indicates whether there are more pages available."
    )
    numbers: Optional[List[NumbersRes]] = Field(
        None, description="List of phone number entries."
    )


class NumbersDelRes(NumbersRes):
    """Response model for a deleted phone number entry."""

    sys_deleted_at: datetime = Field(
        ..., description="Timestamp when the entry was deleted."
    )
    sys_deleted_by: Optional[UUID4] = Field(
        None, description="UUID of the user who deleted the entry."
    )

    class Config:
        from_attributes = True
