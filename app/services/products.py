from typing import Annotated, Literal, Optional

from fastapi import Depends, status
from pydantic import UUID4
from sqlalchemy import Select, and_, func, update
from sqlalchemy.ext.asyncio import AsyncSession

import app.models.products as m_products
import app.schemas.products as s_products

from ..constants import constants as cnst
from ..database.database import Operations, get_db
from ..utilities.utilities import DataUtils as di


class ProductModel:
    products = m_products.Products


class ProductsStatements:
    pass

    class SelectStatements:
        def __init__(self) -> None:
            pass

        @staticmethod
        def sel_prod_by_uuid(product_uuid: UUID4):
            products = ProductModel.products
            statement = Select(products).where(products.uuid == product_uuid)
            return statement

        @staticmethod
        def sel_prod_by_name(product_name: str):
            products = ProductModel.products
            statement = Select(products).where(products.name == product_name)
            return statement

        @staticmethod
        def sel_prods(limit: int, offset: int):
            products = ProductModel.products
            statement = (
                Select(products)
                .where(products.sys_deleted_at == None)
                .offset(offset=offset)
                .limit(limit=limit)
            )
            return statement

        @staticmethod
        def sel_prods_ct():
            products = ProductModel.products
            statement = (
                Select(func.count())
                .select_from(products)
                .where(products.sys_deleted_at == None)
            )
            return statement

    class UpdateStatements:
        def __init__(self) -> None:
            pass

        @staticmethod
        def update_prod_stm(product_uuid: UUID4, product_data: object):
            products = ProductModel.products
            statement = (
                update(products)
                .where(
                    and_(
                        products.uuid == product_uuid,
                    )
                )
                .values(di.set_empty_strs_null(product_data))
                .returning(products)
            )

            return statement


class ProductsServices:
    pass

    class ReadService:
        def __init__(self) -> None:
            pass

        async def get_product(
            self, product_uuid: UUID4, db: AsyncSession = Depends(get_db)
        ):
            statement = ProductsStatements.SelectStatements.sel_prod_by_uuid(
                product_uuid=product_uuid
            )
            product = await Operations.return_one_row(
                service=cnst.PRODUCTS_READ_SERV, statement=statement, db=db
            )
            di.rec_not_exist_or_soft_del(product)
            return product

        async def get_products(
            self, limit: int, offset: int, db: AsyncSession = Depends(get_db)
        ):
            statemenet = ProductsStatements.SelectStatements.sel_prods(
                limit=limit, offset=offset
            )
            products = await Operations.return_all_rows(
                service=cnst.PRODUCTS_READ_SERV, statement=statemenet, db=db
            )
            return products

        async def get_products_ct(self, db: AsyncSession = Depends(get_db)):
            statemenet = ProductsStatements.SelectStatements.sel_prods_ct()
            products = await Operations.return_count(
                service=cnst.PRODUCTS_READ_SERV, statement=statemenet, db=db
            )
            return products

    class CreateService:
        def __init__(self) -> None:
            pass

        async def create_product(
            self,
            product_data: s_products.ProductsCreate,
            transaction_type: Optional[bool] = True,
            db: AsyncSession = Depends(get_db),
        ):
            products = ProductModel.products

            if transaction_type:
                statement = ProductsStatements.SelectStatements.sel_prod_by_name(
                    product_name=product_data.name
                )
                product_exists = await Operations.return_one_row(
                    service=cnst.PRODUCTS_CREATE_SERV, statement=statement, db=db
                )
                di.record_exists(model=product_exists)
                product = await Operations.add_instance(
                    service=cnst.PRODUCTS_CREATE_SERV,
                    model=products,
                    data=product_data,
                    db=db,
                )
                return product
            product = await Operations.add_instance(
                service=cnst.PRODUCTS_CREATE_SERV,
                model=products,
                data=product_data,
                db=db,
            )
            return product

    class UpdateService:
        def __init__(self) -> None:
            pass

        # TODO: needs validation for ensuring product name uniqueness or need to abandon all together and just allow duplicates
        # if we abandon, need to abandon at the create service layer as well...
        async def update_product(
            self,
            product_uuid: UUID4,
            product_data: s_products.ProductsUpdate,
            db: AsyncSession = Depends(get_db),
        ):
            statement = ProductsStatements.UpdateStatements.update_prod_stm(
                product_uuid=product_uuid, product_data=product_data
            )
            product = await Operations.return_one_row(
                service=cnst.PRODUCTS_UPDATE_SERV, statement=statement, db=db
            )
            di.rec_not_exist_or_soft_del(product)
            return product

    class DelService:
        def __init__(self) -> None:
            pass

        async def soft_del_product(
            self,
            product_uuid: UUID4,
            product_data: s_products.ProductsDel,
            db: AsyncSession = Depends(get_db),
        ):
            statement = ProductsStatements.UpdateStatements.update_prod_stm(
                product_uuid=product_uuid, product_data=product_data
            )
            product = await Operations.return_one_row(
                service=cnst.PRODUCTS_DEL_SERV, statement=statement, db=db
            )
            di.record_not_exist(product)
            return product
