from typing import Literal

from fastapi import Depends
from pydantic import UUID4
from sqlalchemy import Select, and_, func, update, values
from sqlalchemy.ext.asyncio import AsyncSession

from ..constants import constants as cnst
from ..database.database import Operations, get_db
from ..exceptions import AddressExists, AddressNotExist
from ..models import addresses as m_addresses
from ..schemas import addresses as s_addresses
from ..utilities.logger import logger
from ..utilities.utilities import DataUtils as di


class AddressesModels:
    addresses = m_addresses.Addresses


class AddressesStatements:
    pass

    class SelStatements:
        pass

        @staticmethod
        def sel_address_by_uuid(
            parent_uuid: UUID4,
            parent_table: Literal["entities", "accounts"],
            address_uuid: UUID4,
        ):
            addresses = AddressesModels.addresses
            statement = Select(addresses).where(
                and_(
                    addresses.parent_uuid == parent_uuid,
                    addresses.uuid == address_uuid,
                    addresses.parent_table == parent_table,
                    addresses.sys_deleted_at == None,
                )
            )
            return statement

        @staticmethod
        def sel_address_by_address(
            parent_uuid: UUID4,
            address_line1: str,
            address_line2: str,
            city: str,
        ):
            addresses = AddressesModels.addresses
            statement = Select(addresses).where(
                and_(
                    addresses.parent_uuid == parent_uuid,
                    addresses.address_line1 == address_line1,
                    addresses.address_line2 == address_line2,
                    addresses.city == city,
                    addresses.sys_deleted_at == None,
                )
            )
            return statement

        @staticmethod
        def sel_address_by_entity(
            parent_uuid: UUID4,
            parent_table: Literal["entities", "accounts"],
            offset: int,
            limit: int,
        ):
            addresses = AddressesModels.addresses
            statement = (
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
            return statement

        @staticmethod
        def sel_address_by_entity_ct(
            parent_uuid: UUID4,
            parent_table: Literal["entities", "accounts"],
        ):
            addresses = AddressesModels.addresses
            statement = (
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
            return statement

    class UpdateStatements:
        pass

        @staticmethod
        def Update_address_by_uuid(
            parent_uuid: UUID4,
            addresses_uuid: UUID4,
            parent_table: Literal["entities", "accounts"],
            address_data: object,
        ):
            addresses = AddressesModels.addresses
            statement = (
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
            return statement


class AddressesServices:
    pass

    class ReadService:
        def __init__(self) -> None:
            pass

        async def get_address(
            self,
            parent_uuid: UUID4,
            parent_table: Literal["entities", "accounts"],
            address_uuid: UUID4,
            db: AsyncSession = Depends(get_db),
        ):
            statement = AddressesStatements.SelStatements.sel_address_by_uuid(
                parent_uuid=parent_uuid,
                address_uuid=address_uuid,
                parent_table=parent_table,
            )
            address = await Operations.return_one_row(
                service=cnst.ADDRESSES_READ_SERVICE, statement=statement, db=db
            )
            return di.record_not_exist(instance=address, exception=AddressNotExist)

        async def get_addresses(
            self,
            parent_uuid: UUID4,
            parent_table: Literal["entities", "accounts"],
            limit: int,
            offset: int,
            db: AsyncSession = Depends(get_db),
        ):
            statement = AddressesStatements.SelStatements.sel_address_by_entity(
                parent_uuid=parent_uuid,
                parent_table=parent_table,
                offset=offset,
                limit=limit,
            )
            addresses = await Operations.return_all_rows(
                service=cnst.ADDRESSES_READ_SERVICE, statement=statement, db=db
            )
            return di.record_not_exist(instance=addresses, exception=AddressNotExist)

        async def get_addresses_ct(
            self,
            entity_uuid: UUID4,
            parent_table: Literal["entities", "accounts"],
            db: AsyncSession = Depends(get_db),
        ):
            statement = AddressesStatements.SelStatements.sel_address_by_entity_ct(
                entity_uuid=entity_uuid, parent_table=parent_table
            )
            return await Operations.return_count(
                service=cnst.ADDRESSES_READ_SERVICE, statement=statement, db=db
            )

    class CreateService:
        def __init__(self) -> None:
            pass

        async def create_address(
            self,
            parent_uuid: UUID4,
            address_data: s_addresses.AddressesCreate,
            db: AsyncSession = Depends(get_db),
        ):
            addresses = AddressesModels.addresses
            statement = AddressesStatements.SelStatements.sel_address_by_address(
                parent_uuid=parent_uuid,
                address_line1=address_data.address_line1,
                address_line2=address_data.address_line2,
                city=address_data.city,
            )
            address_exists = await Operations.return_one_row(
                service=cnst.ADDRESSES_CREATE_SERVICE, statement=statement, db=db
            )
            if not di.record_exists(instance=address_exists, exception=AddressExists):
                address = await Operations.add_instance(
                    service=cnst.ADDRESSES_CREATE_SERVICE,
                    model=addresses,
                    data=address_data,
                    db=db,
                )
                return di.record_not_exist(instance=address, exception=AddressNotExist)

    class UpdateService:
        def __init__(self) -> None:
            pass

        async def update_address(
            self,
            parent_uuid: UUID4,
            parent_table: Literal["entities", "accounts"],
            address_uuid: UUID4,
            address_data: s_addresses.AddressesUpdate,
            db: AsyncSession = Depends(get_db),
        ):
            statement = AddressesStatements.UpdateStatements.Update_address_by_uuid(
                parent_uuid=parent_uuid,
                parent_table=parent_table,
                addresses_uuid=address_uuid,
                address_data=address_data,
            )
            address = await Operations.return_one_row(
                service=cnst.ADDRESSES_UPDATE_SERVICE, statement=statement, db=db
            )
            return di.record_not_exist(instance=address, exception=AddressNotExist)

    class DelService:
        def __init__(self) -> None:
            pass

        async def soft_del_address(
            self,
            parent_uuid: UUID4,
            parent_table: Literal["entities", "accounts"],
            address_uuid: UUID4,
            address_data: s_addresses.AddressesDel,
            db: AsyncSession = Depends(get_db),
        ):
            statement = AddressesStatements.UpdateStatements.Update_address_by_uuid(
                parent_uuid=parent_uuid,
                parent_table=parent_table,
                addresses_uuid=address_uuid,
                address_data=address_data,
            )
            address = await Operations.return_one_row(
                service=cnst.ADDRESSES_DEL_SERVICE, statement=statement, db=db
            )
            return di.record_not_exist(instance=address, exception=AddressNotExist)
