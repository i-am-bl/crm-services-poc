from datetime import datetime
from typing import List, Optional

from pydantic import UUID4, BaseModel, Field

from ._variables import ConstrainedStr, TimeStamp


class WebsitesCreate(BaseModel):
    """Base model for website data, shared across create, update, and response models."""

    entity_uuid: UUID4 = Field(
        ..., description="The UUID of the entity associated with the website."
    )
    sys_value_type_uuid: Optional[UUID4] = Field(
        None,
        description="The UUID of the system value type associated with the website (optional).",
    )
    url: ConstrainedStr = Field(..., description="The URL of the website.")
    description: Optional[ConstrainedStr] = Field(
        None, description="A description of the website (optional)."
    )


class WebsitesInternalCreate(WebsitesCreate):
    """Model for creating a new website record.

    Hides system level fields from client.
    """

    sys_created_by: UUID4 = Field(
        ..., description="The UUID of the user who created the record (optional)."
    )
    sys_created_at: datetime = TimeStamp


class WebsitesUpdate(BaseModel):
    """Model for updating an existing website record."""

    url: Optional[ConstrainedStr] = Field(
        None, description="The updated URL of the website (optional)."
    )
    description: Optional[ConstrainedStr] = Field(
        None, description="The updated description of the website (optional)."
    )
    sys_value_type_uuid: Optional[UUID4] = Field(
        None, description="The updated system value type UUID (optional)."
    )


class WebsitesInternalUpdate(WebsitesUpdate):
    """Model for updating an existing website record.

    Hides system level fields from client.
    """

    sys_updated_at: datetime = TimeStamp
    sys_updated_by: Optional[UUID4] = Field(
        None, description="The UUID of the user who updated the record (optional)."
    )


class WebsitesDel(BaseModel):
    """Model for deleting a website record."""

    sys_deleted_by: Optional[UUID4] = Field(
        None, description="The UUID of the user who deleted the record (optional)."
    )
    sys_deleted_at: datetime = TimeStamp


class WebsitesRes(BaseModel):
    """Response model for website details."""

    id: int = Field(..., description="The ID of the website record.")
    uuid: UUID4 = Field(..., description="The UUID of the website.")
    entity_uuid: UUID4 = Field(
        ..., description="The UUID of the entity associated with the website."
    )
    sys_value_type_uuid: Optional[UUID4] = Field(
        None,
        description="The system value type UUID associated with the website (optional).",
    )
    url: ConstrainedStr = Field(..., description="The URL of the website.")
    description: Optional[ConstrainedStr] = Field(
        None, description="A description of the website (optional)."
    )
    sys_created_by: UUID4 = Field(
        ..., description="The UUID of the user who created the record (optional)."
    )
    sys_created_at: datetime = Field(
        ..., description="Timestamp when the website was created."
    )
    sys_updated_by: Optional[UUID4] = Field(
        None, description="The UUID of the user who last updated the record (optional)."
    )
    sys_updated_at: Optional[datetime] = Field(
        None, description="Timestamp when the website was last updated (optional)."
    )

    class Config:
        from_attributes = True


class WebsitesPgRes(BaseModel):
    """Paginated response model for websites."""

    total: int = Field(..., description="Total number of websites.")
    page: int = Field(..., description="Current page number.")
    limit: int = Field(..., description="Maximum number of websites per page.")
    has_more: bool = Field(
        ..., description="Indicates whether there are more pages available."
    )
    websites: Optional[List[WebsitesRes]] = Field(
        None, description="List of website records in the current page."
    )


class WebsiteDelRes(WebsitesRes):
    """Response model for a deleted website record."""

    sys_deleted_by: Optional[UUID4] = Field(
        None, description="The UUID of the user who deleted the record (optional)."
    )
    sys_deleted_at: datetime = Field(
        ..., description="Timestamp when the website was deleted."
    )

    class Config:
        from_attributes = True
