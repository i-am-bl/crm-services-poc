from datetime import date, datetime
from typing import List, Optional

from pydantic import UUID4, BaseModel, Field

from ._variables import TimeStamp
from .products import ProductsRes


class AccountProducts(BaseModel):
    """
    Model representing an account product with associated product and contract dates.
    """

    account_uuid: UUID4 = Field(..., description="UUID of the associated account.")
    product_uuid: UUID4 = Field(..., description="UUID of the associated product.")
    start_on: Optional[date] = Field(
        None, description="Start date of the account product contract."
    )
    end_on: Optional[date] = Field(
        None, description="End date of the account product contract."
    )


class AccountProductsCreate(AccountProducts):
    """
    Model representing an account product being created, including system metadata.
    """

    sys_created_at: datetime = Field(
        TimeStamp, description="Timestamp of when the account product was created."
    )
    sys_created_by: Optional[UUID4] = Field(
        None,
        description="UUID of the user who created the account product.",
    )


class AccountProductsUpdate(BaseModel):
    """
    Model representing metadata for updating an existing account product.
    """

    start_on: Optional[date] = Field(
        None, description="Start date of the account product contract."
    )
    end_on: Optional[date] = Field(
        None, description="End date of the account product contract."
    )
    sys_updated_at: datetime = Field(
        TimeStamp, description="Timestamp of when the account product was last updated."
    )
    sys_updated_by: Optional[UUID4] = Field(
        None,
        description="UUID of the user who last updated the account product.",
    )


class AccountProductsDel(BaseModel):
    """
    Model representing metadata for deleting an account product.
    """

    sys_deleted_at: datetime = Field(
        TimeStamp, description="Timestamp of when the account product was deleted."
    )
    sys_deleted_by: Optional[UUID4] = Field(
        None,
        description="UUID of the user who deleted the account product.",
    )


class AccountProductsRes(BaseModel):
    """
    Model representing the response data for an account product.
    """

    id: int = Field(..., description="Unique identifier of the account product entry.")
    uuid: UUID4 = Field(..., description="UUID of the account product.")
    account_uuid: UUID4 = Field(..., description="UUID of the associated account.")
    product_uuid: UUID4 = Field(..., description="UUID of the associated product.")
    start_on: Optional[date] = Field(
        None, description="Start date of the account product contract."
    )
    end_on: Optional[date] = Field(
        None, description="End date of the account product contract."
    )
    sys_created_at: datetime = Field(
        ..., description="Timestamp of when the account product was created."
    )
    sys_created_by: Optional[UUID4] = Field(
        None,
        description="UUID of the user who created the account product.",
    )
    sys_updated_at: Optional[datetime] = Field(
        None,
        description="Timestamp of when the account product was last updated.",
    )
    sys_updated_by: Optional[UUID4] = Field(
        None,
        description="UUID of the user who last updated the account product.",
    )

    class Config:
        from_attributes = True


class AccountProductsOrchPgRes(BaseModel):
    """
    Represents a paginated response for account products.
    """

    total: int = Field(..., description="Total number of account products available.")
    page: int = Field(..., description="Current page number.")
    limit: int = Field(..., description="Number of account products per page.")
    has_more: bool = Field(
        ...,
        description="Indicates if there are more account products available beyond the current page.",
    )
    data: Optional[List[ProductsRes]] = Field(
        None,
        description="List of product responses associated with the account products.",
    )


class AccountProductsPgRes(BaseModel):
    """
    Represents a paginated response for account products.
    """

    total: int = Field(..., description="Total number of account products available.")
    page: int = Field(..., description="Current page number.")
    limit: int = Field(..., description="Number of account products per page.")
    has_more: bool = Field(
        ...,
        description="Indicates if there are more account products available beyond the current page.",
    )
    account_products: Optional[List[AccountProductsRes]] = Field(
        None, description="List of account product responses."
    )


class AccountProductsDelRes(AccountProductsRes):
    """
    Represents the response data for a deleted account product, including deletion metadata.
    """

    sys_deleted_at: Optional[datetime] = Field(
        None, description="Timestamp of when the account product was deleted."
    )
    sys_deleted_by: Optional[UUID4] = Field(
        None,
        description="UUID of the user who deleted the account product.",
    )

    class Config:
        from_attributes = True
