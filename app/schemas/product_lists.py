from datetime import date, datetime
from typing import List, Optional

from pydantic import UUID4, BaseModel, Field

from ._variables import ConstrainedStr, TimeStamp


class ProductListsCreate(BaseModel):
    """Model representing a product list."""

    owner_uuid: Optional[UUID4] = Field(
        None, description="The UUID of the owner of the product list."
    )
    name: ConstrainedStr = Field(..., description="The name of the product list.")
    start_on: Optional[date] = Field(
        None, description="The start date when the product list is valid."
    )
    end_on: Optional[date] = Field(
        None, description="The end date when the product list is no longer valid."
    )


class ProductListsInternalCreate(ProductListsCreate):
    """Model for creating a new product list, inheriting from `ProductLists`.

    Hides system level fields from client.
    """

    sys_created_at: datetime = Field(
        ...,
        description="The timestamp when the product list was created, automatically set.",
    )
    sys_created_by: UUID4 = Field(
        ..., description="The UUID of the user who created the product list."
    )


class ProductListsUpdate(ProductListsCreate):
    """Model for updating an existing product list, inheriting from `ProductListsCreate`."""

    owner_uuid: Optional[UUID4] = Field(
        None,
        description="The UUID of the owner of the product list (optional for update).",
    )
    name: Optional[ConstrainedStr] = Field(
        None, description="The name of the product list (optional for update)."
    )
    start_on: Optional[date] = Field(
        None,
        description="The start date when the product list is valid (optional for update).",
    )
    end_on: Optional[date] = Field(
        None,
        description="The end date when the product list is no longer valid (optional for update).",
    )


class ProductListsInternalUpdate(ProductListsUpdate):
    """Model for updating an existing product list, inheriting from `ProductListsCreate`.

    Hides system level fields from client.
    """

    sys_updated_at: datetime = Field(
        ...,
        description="The timestamp when the product list was last updated, automatically set.",
    )
    sys_updated_by: Optional[UUID4] = Field(
        None, description="The UUID of the user who last updated the product list."
    )


class ProductListsDel(BaseModel):
    """Model for deleting a product list."""

    sys_deleted_at: datetime = Field(
        ...,
        description="The timestamp when the product list was deleted, automatically set.",
    )
    sys_deleted_by: Optional[UUID4] = Field(
        None, description="The UUID of the user who deleted the product list."
    )


class ProductListsRes(BaseModel):
    """Model representing a product list with response fields."""

    id: int = Field(..., description="The ID of the product list.")
    uuid: UUID4 = Field(..., description="The UUID of the product list.")
    owner_uuid: Optional[UUID4] = Field(
        None, description="The UUID of the owner of the product list."
    )
    name: Optional[ConstrainedStr] = Field(
        None, description="The name of the product list."
    )
    start_on: Optional[date] = Field(
        None, description="The start date when the product list is valid."
    )
    end_on: Optional[date] = Field(
        None, description="The end date when the product list is no longer valid."
    )
    sys_created_at: datetime = Field(
        ..., description="The timestamp when the product list was created."
    )
    sys_created_by: UUID4 = Field(
        ..., description="The UUID of the user who created the product list."
    )
    sys_updated_at: Optional[datetime] = Field(
        None, description="The timestamp when the product list was last updated."
    )
    sys_updated_by: Optional[UUID4] = Field(
        None, description="The UUID of the user who last updated the product list."
    )

    class Config:
        from_attributes = True


class ProductListsPgRes(BaseModel):
    """Paginated response model for product lists."""

    total: int = Field(..., description="Total number of product lists.")
    page: int = Field(..., description="Current page number.")
    limit: int = Field(..., description="Maximum number of product lists per page.")
    has_more: bool = Field(
        ..., description="Indicates whether there are more pages available."
    )
    product_lists: Optional[List[ProductListsRes]] = Field(
        None, description="List of product lists."
    )


class ProductListsDelRes(ProductListsRes):
    """Response model for deleted product lists."""

    sys_deleted_at: Optional[datetime] = Field(
        None, description="The timestamp when the product list was deleted."
    )
    sys_deleted_by: Optional[UUID4] = Field(
        None, description="The UUID of the user who deleted the product list."
    )

    class Config:
        from_attributes = True
