from datetime import datetime
from typing import List, Literal, Optional

from pydantic import UUID4, BaseModel, Field

from ._variables import TimeStamp
from ..enums.addresses import AddressesParentTable


class Addresses(BaseModel):
    address_line1: Optional[str] = None
    address_line2: Optional[str] = None
    city: Optional[str] = None
    county: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    zip: Optional[str] = None
    zip_plus4: Optional[str] = None


class AccountAddressesCreate(Addresses):

    parent_uuid: UUID4
    parent_table: AddressesParentTable = Field(default=AddressesParentTable.ACCOUNTS)
    sys_value_type_uuid: Optional[UUID4] = None
    sys_created_at: datetime = TimeStamp
    sys_created_by: Optional[UUID4] = None


class EntityAddressesCreate(Addresses):

    parent_uuid: UUID4
    parent_table: AddressesParentTable = Field(default=AddressesParentTable.ENTITIES)
    sys_value_type_uuid: Optional[UUID4] = None
    sys_created_at: datetime = TimeStamp
    sys_created_by: Optional[UUID4] = None


class AddressesUpdate(Addresses):
    sys_value_Type_uuid: Optional[UUID4] = None
    sys_updated_at: datetime = TimeStamp
    sys_updated_by: Optional[UUID4] = None


class AddressesDel(BaseModel):
    sys_deleted_at: datetime = TimeStamp
    sys_deleted_by: Optional[UUID4] = None
    sys_deleted_at: datetime = TimeStamp
    sys_deleted_by: Optional[UUID4] = None


class AddressesRes(BaseModel):
    id: int
    uuid: UUID4
    parent_uuid: UUID4
    parent_table: AddressesParentTable
    address_line1: Optional[str] = None
    address_line2: Optional[str] = None
    city: Optional[str] = None
    county: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    zip: Optional[str] = None
    zip_plus4: Optional[str] = None
    sys_created_at: datetime
    sys_created_by: Optional[UUID4] = None
    sys_updated_at: Optional[datetime] = None
    sys_updated_by: Optional[UUID4] = None

    class Config:
        from_attributes = True


class AddressesDelRes(AddressesRes):
    sys_deleted_at: datetime
    sys_deleted_by: Optional[UUID4] = None

    class Config:
        from_attributes = True


class AddressesPgRes(BaseModel):
    total: int
    page: int
    limit: int
    has_more: bool
    addresses: Optional[List[AddressesRes]] = None
