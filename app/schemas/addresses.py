from datetime import datetime
from typing import List, Optional

from pydantic import UUID4, BaseModel, Field

from ._variables import TimeStamp
from ..enums.addresses import AddressesParentTable


class Addresses(BaseModel):
    """
    Model representing an address, which includes street information, city, state, country, and ZIP code.
    """

    address_line1: Optional[str] = Field(None, description="First line of the address.")
    address_line2: Optional[str] = Field(
        None, description="Second line of the address (e.g., apartment, suite number)."
    )
    city: Optional[str] = Field(None, description="City of the address.")
    county: Optional[str] = Field(None, description="County of the address.")
    state: Optional[str] = Field(None, description="State or province of the address.")
    country: Optional[str] = Field(None, description="Country of the address.")
    zip: Optional[str] = Field(None, description="ZIP or postal code of the address.")
    zip_plus4: Optional[str] = Field(
        None, description="Additional four-digit ZIP+4 code."
    )


class AccountAddressesCreate(Addresses):
    """
    Model for creating an account-related address.
    """

    parent_uuid: UUID4 = Field(..., description="UUID of the associated account.")
    sys_value_type_uuid: Optional[UUID4] = Field(
        None,
        description="UUID representing the type of value associated with the address.",
    )


class AccountAddressesInternalCreate(AccountAddressesCreate):
    """
    Model for internal use only for validating system level fields.
    """

    parent_table: AddressesParentTable = Field(
        default=AddressesParentTable.ACCOUNTS,
        description="Table the address belongs to.",
    )
    sys_created_at: datetime = Field(
        TimeStamp,
        description="Timestamp of when the address was created.",
        exclude=True,
    )
    sys_created_by: Optional[UUID4] = Field(
        None, description="UUID of the user who created the address."
    )


class EntityAddressesCreate(Addresses):
    """
    Model for creating an entity-related address.
    """

    parent_uuid: UUID4 = Field(..., description="UUID of the associated entity.")
    sys_value_type_uuid: Optional[UUID4] = Field(
        None,
        description="UUID representing the type of value associated with the address.",
    )


class EntityAddressesInternalCreate(EntityAddressesCreate):
    """
    Model for internal use only for validating system level fields.
    """

    parent_table: AddressesParentTable = Field(
        default=AddressesParentTable.ENTITIES,
        description="Table the address belongs to.",
    )
    sys_created_at: datetime = Field(
        TimeStamp, description="Timestamp of when the address was created."
    )
    sys_created_by: Optional[UUID4] = Field(
        None, description="UUID of the user who created the address."
    )


class AddressesUpdate(Addresses):
    """
    Model for updating an address.
    """

    sys_value_type_uuid: Optional[UUID4] = Field(
        None,
        description="UUID representing the type of value associated with the address.",
    )


class AddressesInternalUpdate(AddressesUpdate):
    """
    Model for intrnal updating an address hiding system level fields from client.
    """

    sys_updated_at: datetime = Field(
        TimeStamp, description="Timestamp of when the address was last updated."
    )
    sys_updated_by: Optional[UUID4] = Field(
        None, description="UUID of the user who last updated the address."
    )


class AddressesDel(BaseModel):
    """
    Model for deleting an address.
    """

    sys_deleted_at: datetime = Field(
        TimeStamp, description="Timestamp of when the address was deleted."
    )
    sys_deleted_by: Optional[UUID4] = Field(
        None, description="UUID of the user who deleted the address."
    )


class AddressesRes(BaseModel):
    """
    Model representing the response data for an address.
    """

    id: int = Field(..., description="Unique identifier of the address record.")
    uuid: UUID4 = Field(..., description="UUID of the address record.")
    parent_uuid: UUID4 = Field(
        ..., description="UUID of the associated entity or account."
    )
    parent_table: AddressesParentTable = Field(
        ..., description="Table the address belongs to."
    )
    address_line1: Optional[str] = Field(None, description="First line of the address.")
    address_line2: Optional[str] = Field(
        None, description="Second line of the address."
    )
    city: Optional[str] = Field(None, description="City of the address.")
    county: Optional[str] = Field(None, description="County of the address.")
    state: Optional[str] = Field(None, description="State or province of the address.")
    country: Optional[str] = Field(None, description="Country of the address.")
    zip: Optional[str] = Field(None, description="ZIP or postal code of the address.")
    zip_plus4: Optional[str] = Field(
        None, description="Additional four-digit ZIP+4 code."
    )
    sys_created_at: datetime = Field(
        ..., description="Timestamp of when the address was created."
    )
    sys_created_by: Optional[UUID4] = Field(
        None, description="UUID of the user who created the address."
    )
    sys_updated_at: Optional[datetime] = Field(
        None, description="Timestamp of when the address was last updated."
    )
    sys_updated_by: Optional[UUID4] = Field(
        None, description="UUID of the user who last updated the address."
    )

    class Config:
        from_attributes = True


class AddressesDelRes(AddressesRes):
    """
    Model representing the response for a deleted address, including deletion metadata.
    """

    sys_deleted_at: datetime = Field(
        ..., description="Timestamp of when the address was deleted."
    )
    sys_deleted_by: Optional[UUID4] = Field(
        None, description="UUID of the user who deleted the address."
    )

    class Config:
        from_attributes = True


class AddressesPgRes(BaseModel):
    """
    Represents a paginated response for addresses.
    """

    total: int = Field(..., description="Total number of addresses available.")
    page: int = Field(..., description="Current page number.")
    limit: int = Field(..., description="Number of addresses per page.")
    has_more: bool = Field(
        ...,
        description="Indicates if there are more addresses beyond the current page.",
    )
    addresses: Optional[List[AddressesRes]] = Field(
        None, description="List of address response objects."
    )
