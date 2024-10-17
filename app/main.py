from contextlib import asynccontextmanager

from fastapi import FastAPI
from pydantic import UUID4

from . import constants as cnst
from . import models
from .database.database import (
    init_db_table_schema,
    init_db_table_schema_factory,
    init_db_tables,
)
from app.routes.v1.account_contracts import router as account_contracts_router
from app.routes.v1.account_lists import router as account_lists_router
from app.routes.v1.account_products import router as account_products_router
from app.routes.v1.accounts import router as accounts_router
from app.routes.v1.emails import router as emails_router
from app.routes.v1.entities import router as entities_router
from app.routes.v1.entity_accounts import router as entity_accounts_router
from app.routes.v1.individuals import router as individuals_router
from app.routes.v1.invoice_items import router as invoice_items_router
from app.routes.v1.invoices import router as invoices_router
from app.routes.v1.non_individuals import router as non_individuals_router
from app.routes.v1.numbers import router as numbers_router
from app.routes.v1.order_items import router as order_items_router
from app.routes.v1.orders import router as orders_router
from app.routes.v1.product_list_items import router as product_list_items_router
from app.routes.v1.product_lists import router as product_lists_router
from app.routes.v1.products import router as products_router
from app.routes.v1.sys_users import router as sys_users_router
from app.routes.v1.websites import router as websites_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db_table_schema_factory(schemas=cnst.SCHEMAS)
    await init_db_tables(model=models.base)
    yield


app = FastAPI(lifespan=lifespan)

# TODO: Organzie this file
app.include_router(entities_router, tags=["entities"])
app.include_router(sys_users_router, tags=["sys_users"])
app.include_router(emails_router, tags=["emails"])
app.include_router(websites_router, tags=["websites"])
app.include_router(numbers_router, tags=["numbers"])
app.include_router(accounts_router, tags=["accounts"])
app.include_router(products_router, tags=["products"])
app.include_router(product_lists_router, tags=["product_lists"])
app.include_router(product_list_items_router, tags=["product_list_items"])
app.include_router(entity_accounts_router, tags=["entity_accounts"])
app.include_router(non_individuals_router, tags=["non_individuals"])
app.include_router(individuals_router, tags=["individuals"])
app.include_router(account_products_router, tags=["account_products"])
app.include_router(account_contracts_router, tags=["account_contracts"])
app.include_router(account_lists_router, tags=["account_lists"])
app.include_router(orders_router, tags=["orders"])
app.include_router(order_items_router, tags=["order_items"])
app.include_router(invoices_router, tags=["invoices"])
app.include_router(invoice_items_router, tags=["invoice_items"])
