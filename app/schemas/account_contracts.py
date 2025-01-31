from datetime import date, datetime
from typing import List, Optional

from pydantic import UUID4, BaseModel, Field

from ._variables import TimeStamp


class AccountContractsCreate(BaseModel):
    """
    Model representing an account contract with basic details.
    """

    account_uuid: UUID4 = Field(..., description="Unique identifier of the account.")
    start_on: Optional[date] = Field(
        description="Start date of the contract.", default=None
    )
    end_on: Optional[date] = Field(
        description="End date of the contract.", default=None
    )


class AccountContractsInternalCreate(AccountContractsCreate):
    """
    Model representing an account contract being created, including system metadata.
    """

    sys_created_at: datetime = Field(
        TimeStamp, description="Timestamp of when the contract was created."
    )
    sys_created_by: Optional[UUID4] = Field(
        description="UUID of the user who created the contract.", default=None
    )


class AccountContractsUpdate(BaseModel):
    """
    Model representing metadata for updating an existing account contract.
    """

    sys_updated_at: datetime = Field(
        TimeStamp, description="Timestamp of when the contract was last updated."
    )
    sys_updated_by: Optional[UUID4] = Field(
        description="UUID of the user who last updated the contract.",
        default=None,
    )


class AccountContractsDel(BaseModel):
    """
    Model representing metadata for deleting an account contract.
    """

    sys_deleted_at: datetime = Field(
        TimeStamp, description="Timestamp of when the contract was deleted."
    )
    sys_deleted_by: Optional[UUID4] = Field(
        description="UUID of the user who deleted the contract.", default=None
    )


class AccountContractsRes(BaseModel):
    """
    Model representing the response data for an account contract.
    """

    id: int = Field(..., description="Unique identifier of the account contract.")
    uuid: UUID4 = Field(..., description="UUID of the account contract.")
    account_uuid: UUID4 = Field(..., description="UUID of the associated account.")
    start_on: Optional[date] = Field(
        description="Start date of the contract.", default=None
    )
    end_on: Optional[date] = Field(
        description="End date of the contract.", default=None
    )
    sys_created_at: datetime = Field(
        TimeStamp, description="Timestamp of when the contract was created."
    )
    sys_created_by: Optional[UUID4] = Field(
        description="UUID of the user who created the contract.", default=None
    )
    sys_updated_at: Optional[datetime] = Field(
        description="Timestamp of when the contract was last updated.",
        default=None,
    )
    sys_updated_by: Optional[UUID4] = Field(
        description="UUID of the user who last updated the contract.",
        default=None,
    )

    class Config:
        from_attributes = True


class AccountContractsPgRes(BaseModel):
    """
    Represents a paginated response for account contracts.
    """

    total: int = Field(..., description="Total number of contracts available.")
    page: int = Field(..., description="Current page number.")
    limit: int = Field(..., description="Number of contracts per page.")
    has_more: bool = Field(
        ...,
        description="Indicates if there are more contracts available beyond the current page.",
    )
    account_contracts: List[AccountContractsRes] = Field(
        ..., description="List of account contract responses."
    )


class AccountContractsDelRes(AccountContractsRes):
    """
    Represents the response data for a deleted account contract, including deletion metadata.
    """

    sys_deleted_at: datetime = Field(
        TimeStamp, description="Timestamp of when the contract was deleted."
    )
    sys_deleted_by: Optional[UUID4] = Field(
        None, description="UUID of the user who deleted the contract."
    )

    class Config:
        from_attributes = True
