from typing import Literal

from pydantic import UUID4
from sqlalchemy import Select, Update, and_, func, update, values
from ..models.addresses import Addresses
from ..utilities.data import set_empty_strs_null


class AddressesStms:
    """
    A class responsible for constructing SQLAlchemy queries and statements for managing addresses.

    ivars:
    ivar: _model: Addresses: An instance of the Addresses model.
    """

    def __init__(self, model: Addresses) -> None:
        """
        Initializes the AddressesStms class.

        :param model: Addresses: An instance of the Addresses model.
        :return None
        """
        self._model: Addresses = model

    @property
    def model(self) -> Addresses:
        """
        Returns the model instance for addresses.

        :return: Addresses: The Addresses model instance.
        """
        return self._model

    def get_address(
        self,
        parent_uuid: UUID4,
        parent_table: Literal["entities", "accounts"],
        address_uuid: UUID4,
    ) -> Select:
        """
        Selects an address by parent_uuid, parent_table, and address_uuid.

        :param parent_uuid: UUID4: The UUID of the parent (entity or account).
        :param parent_table: Literal["entities", "accounts"]: The table name (entities or accounts) associated with the address.
        :param address_uuid: UUID4: The UUID of the address.
        :return: Select: A Select statement for the address.
        """
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
        """
        Selects an address by its specific address fields.

        :param parent_uuid: UUID4: The UUID of the parent (entity or account).
        :param address_line1: str: The first line of the address.
        :param address_line2: str: The second line of the address (if available).
        :param city: str: The city of the address.
        :return: Select: A Select statement for the address.
        """
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
        """
        Selects addresses by parent_uuid and parent_table with pagination support.

        :param parent_uuid: UUID4: The UUID of the parent (entity or account).
        :param parent_table: Literal["entities", "accounts"]: The table name (entities or accounts) associated with the addresses.
        :param offset: int: The number of records to skip.
        :param limit: int: The number of records to return.
        :return: Select: A Select statement for the addresses.
        """
        addresses = self._model
        return (
            Select(addresses)
            .where(
                and_(
                    addresses.parent_uuid == parent_uuid,
                    addresses.parent_table == parent_table,
                    addresses.sys_deleted_at == None,
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
        """
        Selects the count of addresses by parent_uuid and parent_table.

        :param parent_uuid: UUID4: The UUID of the parent (entity or account).
        :param parent_table: Literal["entities", "accounts"]: The table name (entities or accounts) associated with the addresses.
        :return: Select: A Select statement with the count of addresses.
        """
        addresses = self._model
        return (
            select(func.count())
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
        address_uuid: UUID4,
        parent_table: Literal["entities", "accounts"],
        address_data: object,
    ) -> Update:
        """
        Updates an address by parent_uuid, address_uuid, and parent_table.

        :param parent_uuid: UUID4: The UUID of the parent (entity or account).
        :param address_uuid: UUID4: The UUID of the address.
        :param parent_table: Literal["entities", "accounts"]: The table name (entities or accounts) associated with the address.
        :param address_data: object: The data to update the address with.
        :return: Update: An Update statement for the address.
        """
        addresses = self._model
        return (
            update(addresses)
            .where(
                and_(
                    addresses.parent_uuid == parent_uuid,
                    addresses.parent_table == parent_table,
                    addresses.uuid == address_uuid,
                    addresses.sys_deleted_at == None,
                )
            )
            .values(set_empty_strs_null(values=address_data))
            .returning(addresses)
        )
