from datetime import date, datetime
from typing import List, Optional

from pydantic import UUID4, BaseModel, Field

from ._variables import TimeStamp


class Orders(BaseModel):
    """Represents an order, including details such as associated account, invoice, and approval status."""

    account_uuid: UUID4 = Field(..., description="UUID of the associated account.")
    invoice_uuid: Optional[UUID4] = Field(
        None, description="UUID of the associated invoice."
    )
    owner_uuid: Optional[UUID4] = Field(
        None, description="UUID of the owner of the order."
    )
    approved_on: Optional[date] = Field(
        None, description="Date when the order was approved."
    )
    transacted_on: Optional[date] = Field(
        None, description="Date when the transaction occurred."
    )


class OrdersCreate(Orders):
    """Model for creating a new order."""

    sys_created_at: datetime = Field(
        TimeStamp, description="Timestamp when the order was created."
    )
    sys_created_by: Optional[UUID4] = Field(
        None, description="UUID of the user who created the order."
    )


class OrdersUpdate(BaseModel):
    """Model for updating an existing order."""

    owner_uuid: Optional[UUID4] = Field(
        None, description="Updated UUID of the owner of the order."
    )
    approved_by_uuid: Optional[UUID4] = Field(
        None, description="UUID of the user who approved the order."
    )
    approved_on: Optional[date] = Field(
        None, description="Updated approval date of the order."
    )
    sys_updated_at: datetime = Field(
        TimeStamp, description="Timestamp when the order was last updated."
    )
    sys_updated_by: Optional[UUID4] = Field(
        None, description="UUID of the user who last updated the order."
    )


class OrdersDel(BaseModel):
    """Model for marking an order as deleted."""

    sys_deleted_at: datetime = Field(
        TimeStamp, description="Timestamp when the order was deleted."
    )
    sys_deleted_by: Optional[UUID4] = Field(
        None, description="UUID of the user who deleted the order."
    )


class OrdersRes(BaseModel):
    """Response model for an order."""

    id: int = Field(..., description="Database identifier for the order.")
    uuid: UUID4 = Field(..., description="Unique identifier for the order.")
    account_uuid: UUID4 = Field(..., description="UUID of the associated account.")
    invoice_uuid: Optional[UUID4] = Field(
        None, description="UUID of the associated invoice."
    )
    owner_uuid: Optional[UUID4] = Field(
        None, description="UUID of the owner of the order."
    )
    approved_by: Optional[UUID4] = Field(
        None, description="UUID of the user who approved the order."
    )
    approved_on: Optional[date] = Field(None, description="Approval date of the order.")
    sys_created_at: datetime = Field(
        ..., description="Timestamp when the order was created."
    )
    sys_created_by: Optional[UUID4] = Field(
        None, description="UUID of the user who created the order."
    )
    sys_updated_at: Optional[datetime] = Field(
        None, description="Timestamp when the order was last updated."
    )
    sys_updated_by: Optional[UUID4] = Field(
        None, description="UUID of the user who last updated the order."
    )

    class Config:
        from_attributes = True


class OrdersPgRes(BaseModel):
    """Paginated response model for orders."""

    total: int = Field(..., description="Total number of orders.")
    page: int = Field(..., description="Current page number.")
    limit: int = Field(..., description="Maximum number of orders per page.")
    has_more: bool = Field(
        ..., description="Indicates whether there are more pages available."
    )
    orders: Optional[List[OrdersRes]] = Field(None, description="List of orders.")


class OrdersDelRes(OrdersRes):
    """Response model for a deleted order."""

    sys_deleted_at: datetime = Field(
        ..., description="Timestamp when the order was deleted."
    )
    sys_deleted_by: Optional[UUID4] = Field(
        None, description="UUID of the user who deleted the order."
    )

    class Config:
        from_attributes = True
