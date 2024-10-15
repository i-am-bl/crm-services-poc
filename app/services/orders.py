from typing import List

from fastapi import APIRouter, Depends, status
from pydantic import UUID4
from sqlalchemy import Select, and_, func, update, values
from sqlalchemy.ext.asyncio import AsyncSession

import app.constants as cnst
import app.models.orders as m_orders
import app.schemas.orders as s_orders
from app.database.database import Operations, get_db
from app.services.utilities import DataUtils as di


class OrdersModels:
    orders = m_orders.Orders


class OrdersStatements:
    pass

    class SelStatements:
        pass

        @staticmethod
        def sel_order_by_uuid(order_uuid: UUID4):
            orders = OrdersModels.orders
            statement = Select(orders).where(orders.uuid == order_uuid)
            return statement

        @staticmethod
        def sel_orders(limit: int, offset: int):
            orders = OrdersModels.orders
            statement = (
                Select(orders)
                .where(orders.sys_deleted_at == None)
                .offset(offset=offset)
                .limit(limit=limit)
            )
            return statement

        @staticmethod
        def sel_orders_ct():
            orders = OrdersModels.orders
            statement = (
                Select(func.count())
                .select_from(orders)
                .where(orders.sys_deleted_at == None)
            )
            return statement

    class UpdateStatements:
        pass

        @staticmethod
        def update_order_by_uuid(order_uuid: UUID4, order_data: object):
            orders = OrdersModels.orders
            statement = (
                update(orders)
                .where(orders.uuid == order_uuid)
                .values(di.set_empty_strs_null(values=order_data))
                .returning(orders)
            )
            return statement


class OrdersServices:
    pass

    class ReadService:
        def __init__(self) -> None:
            pass

        async def get_order(
            self, order_uuid: UUID4, db: AsyncSession = Depends(get_db)
        ):
            statement = OrdersStatements.SelStatements.sel_order_by_uuid(
                order_uuid=order_uuid
            )
            order = await Operations.return_one_row(
                service=cnst.ORDERS_READ_SERVICE, statement=statement, db=db
            )
            di.rec_not_exist_or_soft_del(model=order)
            return order

        async def get_orders(
            self, limt: int, offset: int, db: AsyncSession = Depends(get_db)
        ):
            statement = OrdersStatements.SelStatements.sel_orders(
                limit=limt, offset=offset
            )
            orders = await Operations.return_all_rows(
                service=cnst.ORDERS_READ_SERVICE, statement=statement, db=db
            )
            di.record_not_exist(model=orders)
            return orders

        async def get_orders_ct(self, db: AsyncSession = Depends(get_db)):
            statement = OrdersStatements.SelStatements.sel_orders_ct()
            orders = await Operations.return_count(
                service=cnst.ORDERS_READ_SERVICE, statement=statement, db=db
            )
            di.record_not_exist(model=orders)
            return orders

    class CreateService:
        def __init__(self) -> None:
            pass

        async def create_order(
            self, order_data: s_orders.OrdersCreate, db: AsyncSession = Depends(get_db)
        ):
            orders = OrdersModels.orders
            order = await Operations.add_instance(
                service=cnst.ORDERS_CREATE_SERVICE, model=orders, data=order_data, db=db
            )
            di.record_not_exist(model=order)
            return order

    # TODO: implement something for updating the invoice fields, will need different schema for this
    class UpdateService:
        def __init__(self) -> None:
            pass

        async def update_order(
            self,
            order_uuid: UUID4,
            order_data: s_orders.OrdersUpdate,
            db: AsyncSession = Depends(get_db),
        ):
            statement = OrdersStatements.UpdateStatements.update_order_by_uuid(
                order_uuid=order_uuid, order_data=order_data
            )
            order = await Operations.return_one_row(
                service=cnst.ORDERS_UPDATE_SERVICE, statement=statement, db=db
            )
            # TODO: implement emthod to disallow updating an order that has been approved or attached to an invoice
            di.rec_not_exist_or_soft_del(model=order)
            return order

    class DelService:
        def __init__(self) -> None:
            pass

        async def soft_del_order(
            self,
            order_uuid: UUID4,
            order_data: s_orders.OrdersDel,
            db: AsyncSession = Depends(get_db),
        ):
            statement = OrdersStatements.UpdateStatements.update_order_by_uuid(
                order_uuid=order_uuid, order_data=order_data
            )
            order = await Operations.return_one_row(
                service=cnst.ORDERS_DEL_SERVICE, statement=statement, db=db
            )
            # TODO: implement emthod to disallow updating an order that has been approved or attached to an invoice
            di.record_not_exist(model=order)
            return order
