from typing import List

from fastapi import Depends
from pydantic import UUID4
from sqlalchemy import Select, and_, func, update
from sqlalchemy.ext.asyncio import AsyncSession

from ..constants import constants as cnst
from ..database.database import Operations, get_db
from ..exceptions import ProductListItemExists, ProductListItemNotExist
from ..models import product_list_items as m_product_list_items
from ..schemas import product_list_items as s_product_list_items
from ..utilities.utilities import DataUtils as di


class ProductListItemsModels:
    product_list_items = m_product_list_items.ProductListItems


class ProductListItemsStatements:
    pass

    class SelStatements:
        pass

        @staticmethod
        def get_pli_by_product_list_pli_uuid(
            product_list_uuid: UUID4, product_list_item_uuid: UUID4
        ):
            product_list_items = ProductListItemsModels.product_list_items
            statement = Select(product_list_items).where(
                and_(
                    product_list_items.product_list_uuid == product_list_uuid,
                    product_list_items.uuid == product_list_item_uuid,
                    product_list_items.sys_deleted_at == None,
                )
            )
            return statement

        @staticmethod
        def get_pli_by_product_list(product_list_uuid: UUID4, limit: int, offset: int):
            product_list_items = ProductListItemsModels.product_list_items
            statement = (
                Select(product_list_items)
                .where(
                    and_(
                        product_list_items.product_list_uuid == product_list_uuid,
                        product_list_items.sys_deleted_at == None,
                    )
                )
                .offset(offset=offset)
                .limit(limit=limit)
            )

            return statement

        @staticmethod
        def get_pli_by_product_list_ct(product_list_uuid: UUID4):
            product_list_items = ProductListItemsModels.product_list_items
            statement = (
                Select(func.count())
                .select_from(product_list_items)
                .where(
                    and_(
                        product_list_items.product_list_uuid == product_list_uuid,
                        product_list_items.sys_deleted_at == None,
                    )
                )
            )

            return statement

        @staticmethod
        def get_pli_by_product_list_product(
            product_list_uuid: UUID4, product_uuid_list: List[UUID4]
        ):
            product_list_items = ProductListItemsModels.product_list_items
            statement = Select(product_list_items).where(
                and_(
                    product_list_items.product_list_uuid == product_list_uuid,
                    product_list_items.product_uuid.in_(product_uuid_list),
                    product_list_items.sys_deleted_at == None,
                ),
            )

            return statement

    class UpdateStatements:
        pass

        @staticmethod
        def update_pli(
            product_list_uuid: UUID4,
            product_list_item_uuid: UUID4,
            product_list_item_data: object,
        ):
            product_list_items = ProductListItemsModels.product_list_items
            statement = (
                update(product_list_items)
                .where(
                    and_(
                        product_list_items.product_list_uuid == product_list_uuid,
                        product_list_items.uuid == product_list_item_uuid,
                        product_list_items.sys_deleted_at == None,
                    )
                )
                .values(di.set_empty_strs_null(product_list_item_data))
                .returning(product_list_items)
            )
            return statement


class ProductListItemsSerivces:
    pass

    class ReadService:
        def __init__(self) -> None:
            pass

        async def get_product_list_item(
            self,
            product_list_uuid: UUID4,
            product_list_item_uuid: UUID4,
            db: AsyncSession = Depends(get_db),
        ):
            statement = ProductListItemsStatements.SelStatements.get_pli_by_product_list_pli_uuid(
                product_list_uuid=product_list_uuid,
                product_list_item_uuid=product_list_item_uuid,
            )
            product_list_item = await Operations.return_one_row(
                service=cnst.PRODUCT_LIST_ITEMS_READ_SERV, statement=statement, db=db
            )
            return di.record_not_exist(
                instance=product_list_item, exception=ProductListItemNotExist
            )

        async def get_product_list_items(
            self,
            product_list_uuid: UUID4,
            limit: int,
            offset: int,
            db: AsyncSession = Depends(get_db),
        ):
            statement = (
                ProductListItemsStatements.SelStatements.get_pli_by_product_list(
                    product_list_uuid=product_list_uuid, limit=limit, offset=offset
                )
            )
            product_list_items = await Operations.return_all_rows(
                service=cnst.PRODUCT_LIST_ITEMS_READ_SERV, statement=statement, db=db
            )
            return di.record_not_exist(
                instance=product_list_items, exception=ProductListItemNotExist
            )

        async def get_product_list_items_ct(
            self,
            product_list_uuid: UUID4,
            db: AsyncSession = Depends(get_db),
        ):
            statement = (
                ProductListItemsStatements.SelStatements.get_pli_by_product_list_ct(
                    product_list_uuid=product_list_uuid
                )
            )
            return await Operations.return_count(
                service=cnst.PRODUCT_LIST_ITEMS_READ_SERV, statement=statement, db=db
            )

    class CreateService:
        def __init__(self) -> None:
            pass

        async def create_product_list_items(
            self,
            product_list_uuid: UUID4,
            product_list_item_data: List[s_product_list_items.ProductListItemsCreate],
            db: AsyncSession = Depends(get_db),
        ):
            product_list_items = ProductListItemsModels.product_list_items

            list_data = [*product_list_item_data]
            product_uuid_list = [dict.product_uuid for dict in list_data]

            statement = ProductListItemsStatements.SelStatements.get_pli_by_product_list_product(
                product_list_uuid=product_list_uuid,
                product_uuid_list=product_uuid_list,
            )
            product_list_item_exists = await Operations.return_one_row(
                service=cnst.PRODUCT_LIST_ITEMS_CREATE_SERV,
                statement=statement,
                db=db,
            )
            di.record_exists(
                instance=product_list_item_exists, exception=ProductListItemExists
            )
            product_list_item = await Operations.add_instances(
                service=cnst.PRODUCT_LIST_ITEMS_CREATE_SERV,
                model=product_list_items,
                data=product_list_item_data,
                db=db,
            )
            return di.record_not_exist(
                instance=product_list_item, exception=ProductListItemNotExist
            )

    class UpdateService:
        def __init__(self) -> None:
            pass

        async def update_product_list_item(
            self,
            product_list_uuid: UUID4,
            product_list_item_uuid: UUID4,
            product_list_item_data: s_product_list_items.ProductListItemsUpdate,
            db: AsyncSession = Depends(get_db),
        ):
            statement = ProductListItemsStatements.UpdateStatements.update_pli(
                product_list_uuid=product_list_uuid,
                product_list_item_uuid=product_list_item_uuid,
                product_list_item_data=product_list_item_data,
            )
            product_list_item = await Operations.return_one_row(
                service=cnst.PRODUCT_LIST_ITEMS_UPDATE_SERV, statement=statement, db=db
            )
            return di.record_not_exist(
                instance=product_list_item, exception=ProductListItemNotExist
            )

    class DelService:
        def __init__(self) -> None:
            pass

        async def soft_del_product_list_item(
            self,
            product_list_uuid: UUID4,
            product_list_item_uuid: UUID4,
            product_list_item_data: s_product_list_items.ProductListItemsDel,
            db: AsyncSession = Depends(get_db),
        ):
            statement = ProductListItemsStatements.UpdateStatements.update_pli(
                product_list_uuid=product_list_uuid,
                product_list_item_uuid=product_list_item_uuid,
                product_list_item_data=product_list_item_data,
            )
            product_list_item = await Operations.return_one_row(
                service=cnst.PRODUCT_LIST_ITEMS_UPDATE_SERV, statement=statement, db=db
            )
            return di.record_not_exist(
                instance=product_list_item, exception=ProductListItemNotExist
            )
