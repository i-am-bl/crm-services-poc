from operator import and_
from typing import List

from fastapi import Depends, status
from pydantic import UUID4
from sqlalchemy import Select, func, update
from sqlalchemy.ext.asyncio import AsyncSession

from ..constants import constants as cnst
from ..database.database import Operations, get_db
from ..exceptions import OrderItemExists, OrderItemNotExist
from ..models import order_items as m_order_items
from ..schemas import order_items as s_order_items
from ..utilities.utilities import DataUtils as di


class OrderItemsModels:
    order_items = m_order_items.OrderItems


class OrderItemsStatements:
    pass

    class SelStatements:
        pass

        @staticmethod
        def sel_order_item_by_uuid(order_uuid: UUID4, order_item_uuid: UUID4):
            order_items = OrderItemsModels.order_items
            statement = Select(order_items).where(
                and_(
                    order_items.order_uuid == order_uuid,
                    order_items.uuid == order_item_uuid,
                    order_items.sys_deleted_at == None,
                )
            )
            return statement

        @staticmethod
        def sel_order_items_by_order(order_uuid: UUID4, limit: int, offset: int):
            order_items = OrderItemsModels.order_items
            statement = (
                Select(order_items)
                .where(
                    and_(
                        order_items.order_uuid == order_uuid,
                        order_items.sys_deleted_at == None,
                    )
                )
                .offset(offset=offset)
                .limit(limit=limit)
            )
            return statement

        @staticmethod
        def sel_order_items_by_order_ct(order_uuid: UUID4):
            order_items = OrderItemsModels.order_items
            statement = (
                Select(func.count())
                .select_from(order_items)
                .where(
                    and_(
                        order_items.order_uuid == order_uuid,
                        order_items.sys_deleted_at == None,
                    )
                )
            )
            return statement

    class UpdateStatements:
        pass

        @staticmethod
        def update_order_item_by_uuid(
            order_uuid: UUID4, order_item_uuid: UUID4, order_item_data: object
        ):
            order_items = OrderItemsModels.order_items
            statement = (
                update(order_items)
                .where(
                    and_(
                        order_items.order_uuid == order_uuid,
                        order_items.uuid == order_item_uuid,
                        order_items.sys_deleted_at == None,
                    )
                )
                .values(di.set_empty_strs_null(values=order_item_data))
                .returning(order_items)
            )
            return statement


class OrderItemsServices:
    pass

    class ReadService:
        def __init__(self) -> None:
            pass

        async def get_order_item(
            self,
            order_uuid: UUID4,
            order_item_uuid: UUID4,
            db: AsyncSession = Depends(get_db),
        ):
            statement = OrderItemsStatements.SelStatements.sel_order_item_by_uuid(
                order_uuid=order_uuid, order_item_uuid=order_item_uuid
            )
            order_item = await Operations.return_one_row(
                cnst.ORDERS_ITEMS_READ_SERVICE, statement=statement, db=db
            )
            return di.record_not_exist(instance=order_item, exception=OrderItemNotExist)

        async def get_order_items(
            self,
            order_uuid: UUID4,
            limit: int,
            offset: int,
            db: AsyncSession = Depends(get_db),
        ):
            statement = OrderItemsStatements.SelStatements.sel_order_items_by_order(
                order_uuid=order_uuid, limit=limit, offset=offset
            )
            order_items = await Operations.return_all_rows(
                service=cnst.ORDERS_ITEMS_READ_SERVICE, statement=statement, db=db
            )
            return di.record_not_exist(
                instance=order_items, exception=OrderItemNotExist
            )

        async def get_order_items_ct(
            self,
            order_uuid: UUID4,
            db: AsyncSession = Depends(get_db),
        ):
            statement = OrderItemsStatements.SelStatements.sel_order_items_by_order_ct(
                order_uuid=order_uuid
            )
            return await Operations.return_count(
                service=cnst.ORDERS_ITEMS_READ_SERVICE, statement=statement, db=db
            )

    class CreateService:
        def __init__(self) -> None:
            pass

        async def create_order_item(
            self,
            order_uuid: UUID4,
            order_item_data: s_order_items.OrderItemsCreate,
            db: AsyncSession = Depends(get_db),
        ):
            order_items = OrderItemsModels.order_items
            order_item = await Operations.add_instances(
                service=cnst.ORDERS_ITEMS_CREATE_SERVICE,
                model=order_items,
                data=order_item_data,
                db=db,
            )
            return di.record_not_exist(instance=order_item, exception=OrderItemNotExist)

    class UpdateService:
        def __init__(self) -> None:
            pass

        async def update_order_item(
            self,
            order_uuid: UUID4,
            order_item_uuid: UUID4,
            order_item_data: s_order_items.OrderItemsUpdate,
            db: AsyncSession = Depends(get_db),
        ):
            statement = OrderItemsStatements.UpdateStatements.update_order_item_by_uuid(
                order_uuid=order_uuid,
                order_item_uuid=order_item_uuid,
                order_item_data=order_item_data,
            )
            order_item = await Operations.return_one_row(
                service=cnst.ORDERS_ITEMS_UPDATE_SERVICE, statement=statement, db=db
            )
            return di.record_not_exist(instance=order_item, exception=OrderItemNotExist)

    class DelService:
        def __init__(self) -> None:
            pass

        async def soft_del_order_item(
            self,
            order_uuid: UUID4,
            order_item_uuid: UUID4,
            order_item_data: s_order_items.OrderItemsDel,
            db: AsyncSession = Depends(get_db),
        ):
            statement = OrderItemsStatements.UpdateStatements.update_order_item_by_uuid(
                order_uuid=order_uuid,
                order_item_uuid=order_item_uuid,
                order_item_data=order_item_data,
            )
            order_item = await Operations.return_one_row(
                service=cnst.ORDERS_ITEMS_DEL_SERVICE, statement=statement, db=db
            )
            return di.record_not_exist(instance=order_item, exception=OrderItemNotExist)
