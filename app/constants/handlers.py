from fastapi import status

from ..constants import error_codes as err
from ..constants import messages as msg
from ..exceptions import *

handlers = {
    "account_contracts": [
        {
            "class": AccContractNotExist,
            "error_code": err.ACCCOUNT_CONTRACT_NOT_EXIST,
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": msg.ACCCOUNT_CONTRACT_NOT_EXIST,
        },
        {
            "class": AccContractExists,
            "error_code": err.ACCCOUNT_CONTRACT_EXISTS,
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": msg.ACCCOUNT_CONTRACT_EXISTS,
        },
    ],
    "account_lists": [
        {
            "class": AccListNotExist,
            "error_code": err.ACCCOUNT_LIST_NOT_EXIST,
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": msg.ACCCOUNT_LIST_NOT_EXIST,
        },
        {
            "class": AccListExists,
            "error_code": err.ACCCOUNT_LIST_EXISTS,
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": msg.ACCCOUNT_LIST_EXISTS,
        },
    ],
    "account_products": [
        {
            "class": AccProductstNotExist,
            "error_code": err.ACCCOUNT_PRODUCTS_NOT_EXIST,
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": msg.ACCCOUNT_PRODUCTS_NOT_EXIST,
        },
        {
            "class": AccProductsExists,
            "error_code": err.ACCCOUNT_PRODUCTS_EXISTS,
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": msg.ACCCOUNT_PRODUCTS_EXISTS,
        },
    ],
    "accounts": [
        {
            "class": AccsNotExist,
            "error_code": err.ACCCOUNT_NOT_EXIST,
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": msg.ACCCOUNT_NOT_EXIST,
        },
        {
            "class": AccsExists,
            "error_code": err.ACCCOUNT_EXISTS,
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": msg.ACCCOUNT_EXISTS,
        },
    ],
    "auth": [
        {
            "class": InvalidCredentials,
            "error_code": err.INVALID_CREDENTIALS,
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": msg.INVALID_CREDENTIALS,
        },
    ],
    "emails": [
        {
            "class": EmailNotExist,
            "error_code": err.EMAIL_NOT_EXIST,
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": msg.EMAIL_NOT_EXIST,
        },
        {
            "class": EmailExists,
            "error_code": err.EMAIL_EXISTS,
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": msg.EMAIL_EXISTS,
        },
    ],
    "entities": [
        {
            "class": EntityNotExist,
            "error_code": err.ENTITY_NOT_EXIST,
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": msg.ENTITY_NOT_EXIST,
        },
        {
            "class": EntityExists,
            "error_code": err.ENTITY_EXISTS,
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": msg.ENTITY_EXISTS,
        },
    ],
    "entity_accounts": [
        {
            "class": EntityAccNotExist,
            "error_code": err.ENTITY_ACCOUNT_NOT_EXIST,
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": msg.ENTITY_ACCOUNT_NOT_EXIST,
        },
        {
            "class": EntityAccExists,
            "error_code": err.ENTITY_ACCOUNT_EXISTS,
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": msg.ENTITY_ACCOUNT_EXISTS,
        },
    ],
    "individuals": [
        {
            "class": IndividualNotExist,
            "error_code": err.INDIVIDUAL_NOT_EXIST,
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": msg.INDIVIDUAL_NOT_EXIST,
        },
        {
            "class": IndividualExists,
            "error_code": err.INDIVIDUAL_EXISTS,
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": msg.INDIVIDUAL_EXISTS,
        },
    ],
    "invoices": [
        {
            "class": InvoiceNotExist,
            "error_code": err.INVOICE_NOT_EXIST,
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": msg.INVOICE_NOT_EXIST,
        },
        {
            "class": InvoiceExists,
            "error_code": err.INVOICE_EXISTS,
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": msg.INVOICE_EXISTS,
        },
    ],
    "non_individuals": [
        {
            "class": NonIndividualNotExist,
            "error_code": err.NON_INDIVIDUAL_NOT_EXIST,
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": msg.NON_INDIVIDUAL_NOT_EXIST,
        },
        {
            "class": NonIndividualExists,
            "error_code": err.NON_INDIVIDUAL_EXISTS,
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": msg.NON_INDIVIDUAL_EXISTS,
        },
    ],
    "numbers": [
        {
            "class": NumbersNotExist,
            "error_code": err.NUMBER_NOT_EXIST,
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": msg.NUMBER_NOT_EXIST,
        },
        {
            "class": NumberExists,
            "error_code": err.NUMBER_EXISTS,
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": msg.NUMBER_EXISTS,
        },
    ],
    "order_items": [
        {
            "class": OrderItemNotExist,
            "error_code": err.ORDER_ITEM_NOT_EXIST,
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": msg.ORDER_ITEM_NOT_EXIST,
        },
        {
            "class": OrderItemExists,
            "error_code": err.ORDER_ITEM_EXISTS,
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": msg.ORDER_ITEM_EXISTS,
        },
    ],
    "orders": [
        {
            "class": OrderNotExist,
            "error_code": err.ORDER_NOT_EXIST,
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": msg.ORDER_NOT_EXIST,
        },
        {
            "class": OrderExists,
            "error_code": err.ORDER_EXISTS,
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": msg.ORDER_EXISTS,
        },
    ],
    "product_list_items": [
        {
            "class": ProductListItemNotExist,
            "error_code": err.PRODUCT_LIST_ITEM_NOT_EXIST,
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": msg.PRODUCT_LIST_ITEM_NOT_EXIST,
        },
        {
            "class": ProductListItemExists,
            "error_code": err.PRODUCT_LIST_ITEM_EXISTS,
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": msg.PRODUCT_LIST_ITEM_EXISTS,
        },
    ],
    "product_lists": [
        {
            "class": ProductListNotExist,
            "error_code": err.PRODUCT_LIST_NOT_EXIST,
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": msg.PRODUCT_LIST_NOT_EXIST,
        },
        {
            "class": ProductListExists,
            "error_code": err.PRODUCT_LIST_EXISTS,
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": msg.PRODUCT_LIST_EXISTS,
        },
    ],
    "products": [
        {
            "class": ProductsNotExist,
            "error_code": err.PRODUCT_NOT_EXIST,
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": msg.PRODUCT_NOT_EXIST,
        },
        {
            "class": ProductsExists,
            "error_code": err.PRODUCT_EXISTS,
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": msg.PRODUCT_EXISTS,
        },
    ],
    "sys_users": [
        {
            "class": SysUserNotExist,
            "error_code": err.SYS_USER_NOT_EXIST,
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": msg.SYS_USER_NOT_EXIST,
        },
        {
            "class": SysUserExists,
            "error_code": err.SYS_USER_EXISTS,
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": msg.SYS_USER_EXISTS,
        },
    ],
    "webistes": [
        {
            "class": WebsitesNotExist,
            "error_code": err.WEBSITE_NOT_EXIST,
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": msg.WEBSITE_NOT_EXIST,
        },
        {
            "class": WebsitesExists,
            "error_code": err.WEBSITE_EXISTS,
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": msg.WEBSITE_EXISTS,
        },
    ],
    "unhandled": [
        {
            "class": UnhandledException,
            "error_code": err.UNHANDLED_EXCEPTION,
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": msg.UNHANDLED_EXCEPTION,
        },
    ],
}
