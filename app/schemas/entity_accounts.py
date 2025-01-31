from datetime import date, datetime
from typing import List, Optional

from pydantic import UUID4, BaseModel, Field

from ._variables import TimeStamp
from .accounts import AccountsRes
from .entities import IndividualNonIndividualRes


class EntityAccounts(BaseModel):
    """Represents the association between an entity and an account."""

    entity_uuid: UUID4 = Field(..., description="Unique identifier of the entity.")
    account_uuid: UUID4 = Field(..., description="Unique identifier of the account.")
    start_on: Optional[date] = Field(
        None, description="Start date of the entity-account association."
    )
    end_on: Optional[date] = Field(
        None, description="End date of the entity-account association."
    )


class EntityAccountsCreate(EntityAccounts):
    """Model for creating an entity-account association."""

    sys_created_at: datetime = Field(
        TimeStamp, description="Timestamp when the record was created."
    )
    sys_created_by: Optional[UUID4] = Field(
        None, description="UUID of the user who created the record."
    )


class AccountEntityCreate(BaseModel):
    """Model for creating an account-entity association."""

    entity_uuid: UUID4 = Field(..., description="Unique identifier of the entity.")
    account_uuid: Optional[UUID4] = Field(
        None, description="Unique identifier of the account."
    )
    start_on: Optional[date] = Field(None, description="Start date of the association.")
    end_on: Optional[date] = Field(None, description="End date of the association.")


class AccountEntityInternalCreate(AccountEntityCreate):
    """Model for creating an account-entity association hiding system level fields from the client."""

    sys_created_at: datetime = Field(
        TimeStamp, description="Timestamp when the record was created."
    )
    sys_created_by: UUID4 = Field(
        ..., description="UUID of the user who created the record."
    )


class EntityAccountsUpdate(BaseModel):
    """Model for updating an entity-account association."""

    start_on: Optional[date] = Field(
        None, description="Updated start date of the association."
    )
    end_on: Optional[date] = Field(
        None, description="Updated end date of the association."
    )
    sys_updated_at: datetime = Field(
        TimeStamp, description="Timestamp when the record was last updated."
    )
    sys_updated_by: Optional[UUID4] = Field(
        None, description="UUID of the user who last updated the record."
    )


class EntityAccountsInternalUpdate(EntityAccountsUpdate):
    """Model for updating an entity-account association hiding system level fields from the client"""


class EntityAccountsDel(BaseModel):
    """Model for deleting an entity-account association."""

    sys_deleted_at: datetime = Field(
        TimeStamp, description="Timestamp when the record was deleted."
    )
    sys_deleted_by: Optional[UUID4] = Field(
        None, description="UUID of the user who deleted the record."
    )


class EntityAccountsRes(BaseModel):
    """Response model for an entity-account association."""

    id: int = Field(..., description="Unique internal identifier of the record.")
    uuid: UUID4 = Field(
        ..., description="Unique identifier of the entity-account association."
    )
    entity_uuid: UUID4 = Field(..., description="Unique identifier of the entity.")
    account_uuid: UUID4 = Field(..., description="Unique identifier of the account.")
    start_on: Optional[date] = Field(None, description="Start date of the association.")
    end_on: Optional[date] = Field(None, description="End date of the association.")
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


class EntityAccountsPgRes(BaseModel):
    """Paginated response model for entity-account associations."""

    total: int = Field(..., description="Total number of entity-account associations.")
    page: int = Field(..., description="Current page number.")
    limit: int = Field(..., description="Number of records per page.")
    has_more: bool = Field(
        ..., description="Indicates if there are more records available."
    )
    data: List[AccountsRes] = Field(..., description="List of account records.")


class AccountEntitiesPgRes(BaseModel):
    """Paginated response model for account-entity associations."""

    total: int = Field(..., description="Total number of account-entity associations.")
    page: int = Field(..., description="Current page number.")
    limit: int = Field(..., description="Number of records per page.")
    has_more: bool = Field(
        ..., description="Indicates if there are more records available."
    )
    data: List[IndividualNonIndividualRes] = Field(
        ..., description="List of entity records."
    )


class EntityAccountsDelRes(EntityAccountsRes):
    """Response model for a deleted entity-account association."""

    sys_deleted_at: datetime = Field(
        ..., description="Timestamp when the record was deleted."
    )
    sys_deleted_by: Optional[UUID4] = Field(
        None, description="UUID of the user who deleted the record."
    )

    class Config:
        from_attributes = True


class EntityAccountParentRes(BaseModel):
    """Model representing a linked entity-account relationship."""

    account: AccountsRes = Field(..., description="Account details.")
    entity_account: EntityAccountsRes = Field(
        ..., description="Entity account details."
    )
