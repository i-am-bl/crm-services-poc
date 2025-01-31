from datetime import date, datetime
from typing import List, Optional

from pydantic import UUID4, BaseModel, Field

from ._variables import TimeStamp


class InvoicesCreate(BaseModel):
    """Represents an invoice creation request, linking it to an order and tracking status."""

    order_uuid: UUID4 = Field(..., description="UUID of the associated order.")
    sys_value_status_uuid: Optional[UUID4] = Field(
        None, description="UUID representing the status of the invoice."
    )
    transacted_on: Optional[date] = Field(
        None, description="Date when the transaction occurred."
    )
    posted_on: Optional[date] = Field(
        None, description="Date when the invoice was posted."
    )
    paid_on: Optional[date] = Field(None, description="Date when the invoice was paid.")


class InvoicesInternalCreate(InvoicesCreate):
    """Model for internal invoice creation.

    Includes system fields not exposed to external clients.
    """

    sys_created_at: datetime = Field(
        TimeStamp, description="Timestamp when the invoice was created."
    )
    sys_created_by: Optional[UUID4] = Field(
        None, description="UUID of the user who created the invoice."
    )


class InvoicesUpdate(BaseModel):
    """Represents updates to an invoice, including status and payment details."""

    sys_value_status_uuid: Optional[UUID4] = Field(
        None, description="UUID representing the updated status of the invoice."
    )
    transacted_on: Optional[date] = Field(None, description="Updated transaction date.")
    posted_on: Optional[date] = Field(None, description="Updated posted date.")
    paid_on: Optional[date] = Field(None, description="Updated paid date.")
    sys_updated_at: Optional[datetime] = Field(
        None, description="Timestamp when the invoice was last updated."
    )
    sys_updated_by: Optional[UUID4] = Field(
        None, description="UUID of the user who last updated the invoice."
    )


class InvoicesInternalUpdate(InvoicesUpdate):
    """Model for internal invoice updates.

    Includes system fields that track updates.
    """

    sys_updated_at: Optional[datetime] = Field(
        None, description="Timestamp when the invoice was last updated."
    )
    sys_updated_by: Optional[UUID4] = Field(
        None, description="UUID of the user who last updated the invoice."
    )


class InvoicesDel(BaseModel):
    """Represents a soft-delete action on an invoice, tracking deletion metadata."""

    sys_deleted_at: datetime = Field(
        TimeStamp, description="Timestamp when the invoice was deleted."
    )
    sys_deleted_by: Optional[UUID4] = Field(
        None, description="UUID of the user who deleted the invoice."
    )


class InvoicesRes(BaseModel):
    """Represents an invoice response, including all relevant details and system metadata."""

    id: int = Field(..., description="Unique identifier of the invoice.")
    uuid: UUID4 = Field(..., description="UUID of the invoice.")
    order_uuid: UUID4 = Field(..., description="UUID of the associated order.")
    sys_value_status_uuid: Optional[UUID4] = Field(
        None, description="UUID representing the status of the invoice."
    )
    transacted_on: Optional[date] = Field(
        None, description="Date when the transaction occurred."
    )
    posted_on: Optional[date] = Field(
        None, description="Date when the invoice was posted."
    )
    paid_on: Optional[date] = Field(None, description="Date when the invoice was paid.")
    sys_created_at: Optional[datetime] = Field(
        None, description="Timestamp when the invoice was created."
    )
    sys_created_by: Optional[UUID4] = Field(
        None, description="UUID of the user who created the invoice."
    )
    sys_updated_at: Optional[datetime] = Field(
        None, description="Timestamp when the invoice was last updated."
    )
    sys_updated_by: Optional[UUID4] = Field(
        None, description="UUID of the user who last updated the invoice."
    )

    class Config:
        from_attributes = True


class InvoicesPgRes(BaseModel):
    """Represents a paginated response for invoices."""

    total: int = Field(..., description="Total number of invoices available.")
    page: int = Field(..., description="Current page number.")
    limit: int = Field(..., description="Number of invoices per page.")
    has_more: bool = Field(..., description="Indicates if more invoices are available.")
    invoices: Optional[List[InvoicesRes]] = Field(
        None, description="List of invoices in the current page."
    )


class InvoicesDelRes(InvoicesRes):
    """Represents an invoice response including soft-deletion details."""

    sys_deleted_at: datetime = Field(
        TimeStamp, description="Timestamp when the invoice was deleted."
    )
    sys_deleted_by: Optional[UUID4] = Field(
        None, description="UUID of the user who deleted the invoice."
    )

    class Config:
        from_attributes = True
