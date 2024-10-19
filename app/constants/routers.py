# TODO: create a config file for routers

from ..routes.v1.account_contracts import router as account_contracts_router
from ..routes.v1.account_lists import router as account_lists_router
from ..routes.v1.account_products import router as account_products_router
from ..routes.v1.accounts import router as accounts_router
from ..routes.v1.authentication import router as auth_router
from ..routes.v1.emails import router as emails_router
from ..routes.v1.entities import router as entities_router
from ..routes.v1.entity_accounts import router as entity_accounts_router
from ..routes.v1.individuals import router as individuals_router
from ..routes.v1.invoice_items import router as invoice_items_router
from ..routes.v1.invoices import router as invoices_router
from ..routes.v1.non_individuals import router as non_individuals_router
from ..routes.v1.numbers import router as numbers_router
from ..routes.v1.order_items import router as order_items_router
from ..routes.v1.orders import router as orders_router
from ..routes.v1.product_list_items import router as product_list_items_router
from ..routes.v1.product_lists import router as product_lists_router
from ..routes.v1.products import router as products_router
from ..routes.v1.sys_users import router as sys_users_router
from ..routes.v1.websites import router as websites_router


def register_routers(app):
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
    app.include_router(auth_router, tags=["auth"])


routers = {
    [
        {
            "router": entities_router,
            "prefix": "",
            "tags": "",
            "dependencies": "",
            "responses": "",
            "deprecated": "",
            "include_in_schema": "",
            "default_response": "",
            "callbacks": "",
            "generate_unique_id": "",
        },
        {
            "router": sys_users_router,
            "prefix": "",
            "tags": "",
            "dependencies": "",
            "responses": "",
            "deprecated": "",
            "include_in_schema": "",
            "default_response": "",
            "callbacks": "",
            "generate_unique_id": "",
        },
        {
            "router": emails_router,
            "prefix": "",
            "tags": "",
            "dependencies": "",
            "responses": "",
            "deprecated": "",
            "include_in_schema": "",
            "default_response": "",
            "callbacks": "",
            "generate_unique_id": "",
        },
        {
            "router": websites_router,
            "prefix": "",
            "tags": "",
            "dependencies": "",
            "responses": "",
            "deprecated": "",
            "include_in_schema": "",
            "default_response": "",
            "callbacks": "",
            "generate_unique_id": "",
        },
        {
            "router": numbers_router,
            "prefix": "",
            "tags": "",
            "dependencies": "",
            "responses": "",
            "deprecated": "",
            "include_in_schema": "",
            "default_response": "",
            "callbacks": "",
            "generate_unique_id": "",
        },
        {
            "router": accounts_router,
            "prefix": "",
            "tags": "",
            "dependencies": "",
            "responses": "",
            "deprecated": "",
            "include_in_schema": "",
            "default_response": "",
            "callbacks": "",
            "generate_unique_id": "",
        },
        {
            "router": products_router,
            "prefix": "",
            "tags": "",
            "dependencies": "",
            "responses": "",
            "deprecated": "",
            "include_in_schema": "",
            "default_response": "",
            "callbacks": "",
            "generate_unique_id": "",
        },
        {
            "router": product_lists_router,
            "prefix": "",
            "tags": "",
            "dependencies": "",
            "responses": "",
            "deprecated": "",
            "include_in_schema": "",
            "default_response": "",
            "callbacks": "",
            "generate_unique_id": "",
        },
        {
            "router": product_list_items_router,
            "prefix": "",
            "tags": "",
            "dependencies": "",
            "responses": "",
            "deprecated": "",
            "include_in_schema": "",
            "default_response": "",
            "callbacks": "",
            "generate_unique_id": "",
        },
        {
            "router": entity_accounts_router,
            "prefix": "",
            "tags": "",
            "dependencies": "",
            "responses": "",
            "deprecated": "",
            "include_in_schema": "",
            "default_response": "",
            "callbacks": "",
            "generate_unique_id": "",
        },
        {
            "router": non_individuals_router,
            "prefix": "",
            "tags": "",
            "dependencies": "",
            "responses": "",
            "deprecated": "",
            "include_in_schema": "",
            "default_response": "",
            "callbacks": "",
            "generate_unique_id": "",
        },
        {
            "router": individuals_router,
            "prefix": "",
            "tags": "",
            "dependencies": "",
            "responses": "",
            "deprecated": "",
            "include_in_schema": "",
            "default_response": "",
            "callbacks": "",
            "generate_unique_id": "",
        },
        {
            "router": account_contracts_router,
            "prefix": "",
            "tags": "",
            "dependencies": "",
            "responses": "",
            "deprecated": "",
            "include_in_schema": "",
            "default_response": "",
            "callbacks": "",
            "generate_unique_id": "",
        },
        {
            "router": account_products_router,
            "prefix": "",
            "tags": "",
            "dependencies": "",
            "responses": "",
            "deprecated": "",
            "include_in_schema": "",
            "default_response": "",
            "callbacks": "",
            "generate_unique_id": "",
        },
        {
            "router": account_lists_router,
            "prefix": "",
            "tags": "",
            "dependencies": "",
            "responses": "",
            "deprecated": "",
            "include_in_schema": "",
            "default_response": "",
            "callbacks": "",
            "generate_unique_id": "",
        },
        {
            "router": orders_router,
            "prefix": "",
            "tags": "",
            "dependencies": "",
            "responses": "",
            "deprecated": "",
            "include_in_schema": "",
            "default_response": "",
            "callbacks": "",
            "generate_unique_id": "",
        },
        {
            "router": order_items_router,
            "prefix": "",
            "tags": "",
            "dependencies": "",
            "responses": "",
            "deprecated": "",
            "include_in_schema": "",
            "default_response": "",
            "callbacks": "",
            "generate_unique_id": "",
        },
        {
            "router": invoices_router,
            "prefix": "",
            "tags": "",
            "dependencies": "",
            "responses": "",
            "deprecated": "",
            "include_in_schema": "",
            "default_response": "",
            "callbacks": "",
            "generate_unique_id": "",
        },
        {
            "router": invoice_items_router,
            "prefix": "",
            "tags": "",
            "dependencies": "",
            "responses": "",
            "deprecated": "",
            "include_in_schema": "",
            "default_response": "",
            "callbacks": "",
            "generate_unique_id": "",
        },
        {
            "router": auth_router,
            "prefix": "",
            "tags": "",
            "dependencies": "",
            "responses": "",
            "deprecated": "",
            "include_in_schema": "",
            "default_response": "",
            "callbacks": "",
            "generate_unique_id": "",
        },
    ]
}
