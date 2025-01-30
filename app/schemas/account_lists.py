from datetime import date, datetime
from typing import List, Optional

from pydantic import UUID4, BaseModel, Field

from ._variables import TimeStamp
from .product_lists import ProductListsRes


class AccountLists(BaseModel):
    """
    Model representing an account list with associated product list and contract dates.
    """

    account_uuid: UUID4 = Field(..., description="UUID of the associated account.")
    product_list_uuid: UUID4 = Field(
        ..., description="UUID of the associated product list."
    )
    start_on: Optional[date] = Field(
        None, description="Start date of the account list contract."
    )
    end_on: Optional[date] = Field(
        None, description="End date of the account list contract."
    )


class AccountListsCreate(AccountLists):
    """
    Model representing an account list being created, including system metadata.
    """

    sys_created_at: datetime = Field(
        TimeStamp, description="Timestamp of when the account list was created."
    )
    sys_created_by: Optional[UUID4] = Field(
        None, description="UUID of the user who created the account list."
    )


class AccountListsUpdate(BaseModel):
    """
    Model representing metadata for updating an existing account list.
    """

    sys_updated_at: datetime = Field(
        TimeStamp, description="Timestamp of when the account list was last updated."
    )
    sys_updated_by: Optional[UUID4] = Field(
        None,
        description="UUID of the user who last updated the account list.",
    )


class AccountListsDel(BaseModel):
    """
    Model representing metadata for deleting an account list.
    """

    sys_deleted_at: datetime = Field(
        TimeStamp, description="Timestamp of when the account list was deleted."
    )
    sys_deleted_by: Optional[UUID4] = Field(
        None, description="UUID of the user who deleted the account list."
    )


class AccountListsRes(BaseModel):
    """
    Model representing the response data for an account list.
    """

    id: int = Field(..., description="Unique identifier of the account list entry.")
    uuid: UUID4 = Field(..., description="UUID of the account list.")
    account_uuid: UUID4 = Field(..., description="UUID of the associated account.")
    product_list_uuid: UUID4 = Field(
        ..., description="UUID of the associated product list."
    )
    start_on: Optional[date] = Field(
        None, description="Start date of the account list contract."
    )
    end_on: Optional[date] = Field(
        None, description="End date of the account list contract."
    )
    sys_created_at: datetime = Field(
        ..., description="Timestamp of when the account list was created."
    )
    sys_created_by: Optional[UUID4] = Field(
        None, description="UUID of the user who created the account list."
    )
    sys_updated_at: Optional[datetime] = Field(
        None,
        description="Timestamp of when the account list was last updated.",
    )
    sys_updated_by: Optional[UUID4] = Field(
        None,
        description="UUID of the user who last updated the account list.",
    )

    class Config:
        from_attributes = True


class AccountListsOrchPgRes(BaseModel):
    """
    Represents a paginated response for account lists.
    """

    total: int = Field(..., description="Total number of account lists available.")
    page: int = Field(..., description="Current page number.")
    limit: int = Field(..., description="Number of account lists per page.")
    has_more: bool = Field(
        ...,
        description="Indicates if there are more account lists available beyond the current page.",
    )
    data: Optional[List[ProductListsRes]] = Field(
        None,
        description="List of product list responses associated with the account lists.",
    )


class AccountListsDelRes(AccountListsRes):
    """
    Represents the response data for a deleted account list, including deletion metadata.
    """

    sys_deleted_at: datetime = Field(
        TimeStamp, description="Timestamp of when the account list was deleted."
    )
    sys_deleted_by: Optional[UUID4] = Field(
        None, description="UUID of the user who deleted the account list."
    )

    class Config:
        from_attributes = True
