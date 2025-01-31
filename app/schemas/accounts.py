from datetime import date, datetime
from typing import List, Optional

from pydantic import UUID4, BaseModel, Field

from ._variables import ConstrainedStr, TimeStamp


class AccountsCreate(BaseModel):
    """
    Model representing an account with optional name and contract dates.
    """

    name: Optional[ConstrainedStr] = Field(None, description="Name of the account.")
    start_on: Optional[date] = Field(
        None, description="Start date of the account's validity period."
    )
    end_on: Optional[date] = Field(
        None, description="End date of the account's validity period."
    )


class AccountsInternalCreate(AccountsCreate):
    """
    Model representing an account creation request, including system metadata.

    Hiding system level fields from the client.
    """

    sys_created_at: datetime = Field(
        TimeStamp, description="Timestamp of when the account was created."
    )
    sys_created_by: Optional[UUID4] = Field(
        None, description="UUID of the user who created the account."
    )


class AccountsUpdate(BaseModel):
    """
    Model representing metadata for updating an existing account.
    """

    sys_updated_at: datetime = Field(
        TimeStamp, description="Timestamp of when the account was last updated."
    )
    sys_updated_by: Optional[UUID4] = Field(
        None, description="UUID of the user who last updated the account."
    )


class AccountsDel(BaseModel):
    """
    Model representing metadata for deleting an account.
    """

    sys_deleted_at: datetime = Field(
        TimeStamp, description="Timestamp of when the account was deleted."
    )
    sys_deleted_by: Optional[UUID4] = Field(
        None, description="UUID of the user who deleted the account."
    )


class AccountsRes(BaseModel):
    """
    Model representing the response data for an account.
    """

    id: int = Field(..., description="Unique identifier of the account entry.")
    uuid: UUID4 = Field(..., description="UUID of the account.")
    name: Optional[ConstrainedStr] = Field(None, description="Name of the account.")
    start_on: Optional[date] = Field(
        None, description="Start date of the account's validity period."
    )
    end_on: Optional[date] = Field(
        None, description="End date of the account's validity period."
    )
    sys_created_at: datetime = Field(
        ..., description="Timestamp of when the account was created."
    )
    sys_created_by: Optional[UUID4] = Field(
        None, description="UUID of the user who created the account."
    )
    sys_updated_at: Optional[datetime] = Field(
        None,
        description="Timestamp of when the account was last updated.",
    )
    sys_updated_by: Optional[UUID4] = Field(
        None, description="UUID of the user who last updated the account."
    )

    class Config:
        from_attributes = True


class AccountsPgRes(BaseModel):
    """
    Represents a paginated response for accounts.
    """

    total: int = Field(..., description="Total number of accounts available.")
    page: int = Field(..., description="Current page number.")
    limit: int = Field(..., description="Number of accounts per page.")
    has_more: bool = Field(
        ...,
        description="Indicates if there are more accounts available beyond the current page.",
    )
    accounts: List[AccountsRes] = Field(
        ..., description="List of account response objects."
    )

    class Config:
        from_attributes = True


class AccountsDelRes(AccountsRes):
    """
    Represents the response data for a deleted account, including deletion metadata.
    """

    sys_deleted_at: datetime = Field(
        ..., description="Timestamp of when the account was deleted."
    )
    sys_deleted_by: Optional[UUID4] = Field(
        None, description="UUID of the user who deleted the account."
    )

    class Config:
        from_attributes = True
