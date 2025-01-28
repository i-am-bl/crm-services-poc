from typing import Literal

from pydantic import UUID4
from sqlalchemy import Select, Update, and_, func, update, values
from ..models.addresses import Addresses
from ..utilities.utilities import DataUtils as di


class AddressesStms:
    def __init__(self, model: Addresses) -> None:
        self._model: Addresses = model

    @property
    def model(self) -> Addresses:
        return self._model

    def get_address(
        self,
        parent_uuid: UUID4,
        parent_table: Literal["entities", "accounts"],
        address_uuid: UUID4,
    ) -> Select:
        addresses = self._model
        return Select(addresses).where(
            and_(
                addresses.parent_uuid == parent_uuid,
                addresses.uuid == address_uuid,
                addresses.parent_table == parent_table,
                addresses.sys_deleted_at == None,
            )
        )

    def get_address_by_address(
        self,
        parent_uuid: UUID4,
        address_line1: str,
        address_line2: str,
        city: str,
    ) -> Select:
        addresses = self._model
        return Select(addresses).where(
            and_(
                addresses.parent_uuid == parent_uuid,
                addresses.address_line1 == address_line1,
                addresses.address_line2 == address_line2,
                addresses.city == city,
                addresses.sys_deleted_at == None,
            )
        )

    def get_address_by_entity(
        self,
        parent_uuid: UUID4,
        parent_table: Literal["entities", "accounts"],
        offset: int,
        limit: int,
    ) -> Select:
        addresses = self._model
        return (
            (
                Select(addresses).where(
                    and_(
                        addresses.parent_uuid == parent_uuid,
                        addresses.parent_table == parent_table,
                        addresses.sys_deleted_at == None,
                    )
                )
            )
            .offset(offset=offset)
            .limit(limit=limit)
        )

    def get_addresses_ct(
        self,
        parent_uuid: UUID4,
        parent_table: Literal["entities", "accounts"],
    ) -> Select:
        addresses = self._model
        return (
            Select(func.count())
            .select_from(addresses)
            .where(
                and_(
                    addresses.parent_uuid == parent_uuid,
                    addresses.parent_table == parent_table,
                    addresses.sys_deleted_at == None,
                )
            )
        )

    def update_address(
        self,
        parent_uuid: UUID4,
        addresses_uuid: UUID4,
        parent_table: Literal["entities", "accounts"],
        address_data: object,
    ) -> Update:
        addresses = self._model
        return (
            update(addresses)
            .where(
                and_(
                    addresses.parent_uuid == parent_uuid,
                    addresses.parent_table == parent_table,
                    addresses.uuid == addresses_uuid,
                    addresses.sys_deleted_at == None,
                )
            )
            .values(di.set_empty_strs_null(values=address_data))
            .returning(addresses)
        )
