from fastapi import Depends
from pydantic import UUID4
from sqlalchemy import Select, and_, update, func
from sqlalchemy.ext.asyncio import AsyncSession

import app.constants as cnst
import app.models.account_products as m_account_products
import app.schemas.account_products as s_account_products
from app.database.database import Operations, get_db
from app.services.utilities import DataUtils as di


class AccountProductsModels:
    account_products = m_account_products.AccountProducts


class AccountProductStatements:
    pass

    class SelStatements:
        pass

        @staticmethod
        def sel_acc_prod_by_uuid(account_uuid: UUID4, account_product_uuid: UUID4):
            account_products = AccountProductsModels.account_products
            statement = Select(account_products).where(
                and_(
                    account_products.account_uuid == account_uuid,
                    account_products.uuid == account_product_uuid,
                )
            )
            return statement

        @staticmethod
        def sel_acc_prod_by_prod_uuid(account_uuid: UUID4, product_uuid: UUID4):
            account_products = AccountProductsModels.account_products
            statement = Select(account_products).where(
                and_(
                    account_products.account_uuid == account_uuid,
                    account_products.product_uuid == product_uuid,
                    account_products.sys_deleted_at == None,
                )
            )
            return statement

        @staticmethod
        def sel_acc_prod_by_acc_uuid(account_uuid: UUID4, limit: int, offset: int):
            account_products = AccountProductsModels.account_products
            statement = (
                Select(account_products)
                .where(
                    and_(
                        account_products.account_uuid == account_uuid,
                        account_products.sys_deleted_at == None,
                    )
                )
                .offset(offset=offset)
                .limit(limit=limit)
            )
            return statement

        @staticmethod
        def sel_acc_prod_by_acc_ct(account_uuid: UUID4):
            account_products = AccountProductsModels.account_products
            statement = (
                Select(func.count())
                .select_from(account_products)
                .where(
                    and_(
                        account_products.account_uuid == account_uuid,
                        account_products.sys_deleted_at == None,
                    )
                )
            )
            return statement

    class UpdateStatements:
        pass

        @staticmethod
        def update_acc_prod_by_uuid(
            account_uuid: UUID4,
            account_product_uuid: UUID4,
            account_product_data: object,
        ):
            account_products = AccountProductsModels.account_products
            statement = (
                update(account_products)
                .where(
                    and_(
                        account_products.account_uuid == account_uuid,
                        account_products.uuid == account_product_uuid,
                    )
                )
                .values(di.set_empty_strs_null(values=account_product_data))
                .returning(account_products)
            )
            return statement


class AccountProductsServices:
    pass

    class ReadService:
        def __init__(self) -> None:
            pass

        async def get_account_product(
            self,
            account_uuid: UUID4,
            account_product_uuid: UUID4,
            db: AsyncSession = Depends(get_db),
        ):
            statement = AccountProductStatements.SelStatements.sel_acc_prod_by_uuid(
                account_uuid=account_uuid, account_product_uuid=account_product_uuid
            )
            account_product = await Operations.return_one_row(
                service=cnst.ACCOUNTS_PRODUCTS_READ_SERVICE, statement=statement, db=db
            )
            di.record_not_exist(model=account_product)
            return account_product

        async def get_account_products(
            self,
            account_uuid: UUID4,
            limit: int,
            offset: int,
            db: AsyncSession = Depends(get_db),
        ):
            statement = AccountProductStatements.SelStatements.sel_acc_prod_by_acc_uuid(
                account_uuid=account_uuid, limit=limit, offset=offset
            )
            account_products = await Operations.return_all_rows(
                service=cnst.ACCOUNTS_PRODUCTS_READ_SERVICE, statement=statement, db=db
            )
            di.record_not_exist(model=account_products)
            return account_products

        async def get_account_product_ct(
            self, account_uuid: UUID4, db: AsyncSession = Depends(get_db)
        ):
            statement = AccountProductStatements.SelStatements.sel_acc_prod_by_acc_ct(
                account_uuid=account_uuid
            )
            account_products = await Operations.return_count(
                service=cnst.ACCOUNTS_PRODUCTS_READ_SERVICE, statement=statement, db=db
            )

            return account_products

    class CreateService:
        def __init__(self) -> None:
            pass

        async def create_account_product(
            self,
            account_uuid: UUID4,
            account_product_data: s_account_products.AccountProductsCreate,
            db: AsyncSession = Depends(get_db),
        ):
            accont_products = AccountProductsModels.account_products
            statement = (
                AccountProductStatements.SelStatements.sel_acc_prod_by_prod_uuid(
                    account_uuid=account_uuid,
                    product_uuid=account_product_data.product_uuid,
                )
            )
            account_product_exists = await Operations.return_one_row(
                service=cnst.ACCOUNTS_PRODUCTS_CREATE_SERVICE,
                statement=statement,
                db=db,
            )
            di.record_exists(model=account_product_exists)
            account_product = await Operations.add_instance(
                service=cnst.ACCOUNTS_PRODUCTS_CREATE_SERVICE,
                model=accont_products,
                data=account_product_data,
                db=db,
            )
            di.record_not_exist(model=account_product)
            return account_product

    class UpdateService:
        def __init__(self) -> None:
            pass

        async def update_account_product(
            self,
            account_uuid: UUID4,
            account_product_uuid: UUID4,
            account_product_data: s_account_products.AccountProductsUpdate,
            db: AsyncSession = Depends(get_db),
        ):
            statement = (
                AccountProductStatements.UpdateStatements.update_acc_prod_by_uuid(
                    account_uuid=account_uuid,
                    account_product_uuid=account_product_uuid,
                    account_product_data=account_product_data,
                )
            )
            account_product = await Operations.return_one_row(
                service=cnst.ACCOUNTS_PRODUCTS_UPDATE_SERVICE,
                statement=statement,
                db=db,
            )
            di.rec_not_exist_or_soft_del(model=account_product)
            return account_product

    class DelService:
        def __init__(self) -> None:
            pass

        async def soft_del_account_product(
            self,
            account_uuid: UUID4,
            account_product_uuid: UUID4,
            account_product_data: s_account_products.AccountProductsDel,
            db: AsyncSession = Depends(get_db),
        ):
            statement = (
                AccountProductStatements.UpdateStatements.update_acc_prod_by_uuid(
                    account_uuid=account_uuid,
                    account_product_uuid=account_product_uuid,
                    account_product_data=account_product_data,
                )
            )
            account_product = await Operations.return_one_row(
                service=cnst.ACCOUNTS_PRODUCTS_DEL_SERVICE, statement=statement, db=db
            )
            di.record_not_exist(model=account_product)
            return account_product
