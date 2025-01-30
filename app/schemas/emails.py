from datetime import datetime
from typing import List, Optional

from pydantic import UUID4, BaseModel

from ._variables import ConstrainedEmailStr, TimeStamp


from datetime import datetime
from typing import List, Optional

from pydantic import UUID4, BaseModel, Field

from ._variables import ConstrainedEmailStr, TimeStamp


class Emails(BaseModel):
    """
    Base model representing an email.
    """

    email: ConstrainedEmailStr = Field(
        ..., description="Email address with constraints applied."
    )


class EmailsCreate(Emails):
    """
    Model for creating a new email record.
    """

    entity_uuid: UUID4 = Field(..., description="UUID of the associated entity.")
    sys_created_at: datetime = Field(
        TimeStamp, description="Timestamp of when the email record was created."
    )
    sys_created_by: Optional[UUID4] = Field(
        None, description="UUID of the user who created the email record."
    )


class EmailsUpdate(BaseModel):
    """
    Model for updating an existing email record.
    """

    email: Optional[ConstrainedEmailStr] = Field(
        None, description="Updated email address."
    )
    sys_updated_at: datetime = Field(
        TimeStamp, description="Timestamp of when the email record was last updated."
    )
    sys_updated_by: Optional[UUID4] = Field(
        None, description="UUID of the user who last updated the email record."
    )


class EmailsDel(BaseModel):
    """
    Model for deleting an email record.
    """

    sys_deleted_at: datetime = Field(
        TimeStamp, description="Timestamp of when the email record was deleted."
    )
    sys_deleted_by: Optional[UUID4] = Field(
        None, description="UUID of the user who deleted the email record."
    )


class EmailsRes(BaseModel):
    """
    Model representing the response data for an email record.
    """

    id: int = Field(..., description="Unique identifier of the email record.")
    uuid: UUID4 = Field(..., description="UUID of the email record.")
    entity_uuid: UUID4 = Field(..., description="UUID of the associated entity.")
    sys_created_at: datetime = Field(
        ..., description="Timestamp of when the email record was created."
    )
    sys_created_by: Optional[UUID4] = Field(
        None, description="UUID of the user who created the email record."
    )
    sys_updated_at: Optional[datetime] = Field(
        None, description="Timestamp of when the email record was last updated."
    )
    sys_updated_by: Optional[UUID4] = Field(
        None, description="UUID of the user who last updated the email record."
    )

    class Config:
        from_attributes = True


class EmailsPgRes(BaseModel):
    """
    Represents a paginated response for emails.
    """

    total: int = Field(..., description="Total number of email records available.")
    page: int = Field(..., description="Current page number.")
    limit: int = Field(..., description="Number of email records per page.")
    has_more: bool = Field(
        ...,
        description="Indicates if there are more email records beyond the current page.",
    )
    emails: Optional[List[EmailsRes]] = Field(
        None, description="List of email response objects."
    )

    class Config:
        from_attributes = True


class EmailsDelRes(EmailsRes):
    """
    Model representing the response for a deleted email record.
    """

    sys_deleted_at: datetime = Field(
        TimeStamp, description="Timestamp of when the email record was deleted."
    )
    sys_deleted_by: Optional[UUID4] = Field(
        None, description="UUID of the user who deleted the email record."
    )

    class Config:
        from_attributes = True
