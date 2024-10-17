from fastapi import Depends
from pydantic import UUID4
from sqlalchemy import Select, Update, and_, func, update
from sqlalchemy.ext.asyncio import AsyncSession

import app.constants as cnst
import app.models.product_lists as m_product_lists
import app.schemas.product_lists as s_product_lists
from app.database.database import Operations, get_db
from app.logger import logger
from app.services.utilities import DataUtils as di


class ProductListsModels:
    product_lists = m_product_lists.ProductLists


class ProductListStatements:
    pass

    class SelStatements:
        pass

        @staticmethod
        def sel_prod_list_by_uuid(product_list_uuid: UUID4):
            product_lists = ProductListsModels.product_lists
            statement = Select(product_lists).where(
                product_lists.uuid == product_list_uuid
            )
            return statement

        @staticmethod
        def sel_prod_list_by_name(product_list_name: str):
            product_lists = ProductListsModels.product_lists
            statement = Select(product_lists).where(
                and_(
                    product_lists.name == product_list_name,
                    product_lists.sys_deleted_at == None,
                )
            )
            return statement

        @staticmethod
        def sel_prod_lists(limit: int, offset: int):
            product_lists = ProductListsModels.product_lists
            statement = (
                Select(product_lists)
                .where(product_lists.sys_deleted_at == None)
                .offset(offset=offset)
                .limit(limit=limit)
            )
            return statement

        @staticmethod
        def sel_prod_lists_ct():
            product_lists = ProductListsModels.product_lists
            statement = (
                Select(func.count())
                .select_from(product_lists)
                .where(product_lists.sys_deleted_at == None)
            )
            return statement

    class UpdateStatements:
        pass

        @staticmethod
        def update_by_uuid(product_list_uuid: UUID4, product_list_data: object):
            product_lists = ProductListsModels.product_lists
            statement = (
                Update(product_lists)
                .where(product_lists.uuid == product_list_uuid)
                .values(di.set_empty_strs_null(values=product_list_data))
                .returning(product_lists)
            )
            return statement


class ProductListsServices:
    pass

    class ReadService:
        def __init__(self) -> None:
            pass

        async def get_product_list(
            self, product_list_uuid: UUID4, db: AsyncSession = Depends(get_db)
        ):

            statement = ProductListStatements.SelStatements.sel_prod_list_by_uuid(
                product_list_uuid=product_list_uuid
            )
            product_list = await Operations.return_one_row(
                service=cnst.PRODUCT_LISTS_READ_SERV, statement=statement, db=db
            )
            di.rec_not_exist_or_soft_del(product_list)
            return product_list

        async def get_product_lists(
            self, limit: int, offset: int, db: AsyncSession = Depends(get_db)
        ):

            statement = ProductListStatements.SelStatements.sel_prod_lists(
                limit=limit, offset=offset
            )
            product_lists = await Operations.return_all_rows(
                service=cnst.PRODUCT_LISTS_READ_SERV, statement=statement, db=db
            )

            return product_lists

        async def get_product_lists_ct(self, db: AsyncSession = Depends(get_db)):

            statement = ProductListStatements.SelStatements.sel_prod_lists_ct()
            product_lists = await Operations.return_count(
                service=cnst.PRODUCT_LISTS_READ_SERV, statement=statement, db=db
            )

            return product_lists

    class CreateService:
        def __init__(self) -> None:
            pass

        async def create_product_list(
            self,
            product_list_data: s_product_lists.ProductListsCreate,
            db: AsyncSession = Depends(get_db),
        ):
            product_lists = ProductListsModels.product_lists

            statement = ProductListStatements.SelStatements.sel_prod_list_by_name(
                product_list_name=product_list_data.name
            )
            product_list_exists = await Operations.return_one_row(
                service=cnst.PRODUCT_LISTS_CREATE_SERV, statement=statement, db=db
            )
            di.record_exists(product_list_exists)

            product_list = await Operations.add_instance(
                service=cnst.PRODUCT_LISTS_CREATE_SERV,
                model=product_lists,
                data=product_list_data,
                db=db,
            )
            return product_list

    class UpdateService:
        def __init__(self) -> None:
            pass

        async def update_product_list(
            self,
            product_list_uuid: UUID4,
            product_list_data: s_product_lists.ProductListsUpdate,
            db: AsyncSession = Depends(get_db),
        ):
            statement = ProductListStatements.UpdateStatements.update_by_uuid(
                product_list_uuid=product_list_uuid, product_list_data=product_list_data
            )
            product_lists = await Operations.return_one_row(
                service=cnst.PRODUCT_LISTS_UPDATE_SERV, statement=statement, db=db
            )
            di.rec_not_exist_or_soft_del(model=product_lists)
            return product_lists

    class DelService:
        def __init__(self) -> None:
            pass

        async def soft_del_product_list(
            self,
            product_list_uuid: UUID4,
            product_list_data: s_product_lists.ProductListsDel,
            db: AsyncSession = Depends(get_db),
        ):
            statement = ProductListStatements.UpdateStatements.update_by_uuid(
                product_list_uuid=product_list_uuid, product_list_data=product_list_data
            )
            product_lists = await Operations.return_one_row(
                service=cnst.PRODUCT_LISTS_DEL_SERV, statement=statement, db=db
            )
            di.record_not_exist(model=product_lists)
            return product_lists
