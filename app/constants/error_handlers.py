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
            "allow_registration": True,
        },
        {
            "class": AccContractExists,
            "error_code": err.ACCCOUNT_CONTRACT_EXISTS,
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": msg.ACCCOUNT_CONTRACT_EXISTS,
            "allow_registration": True,
        },
    ],
    "account_lists": [
        {
            "class": AccListNotExist,
            "error_code": err.ACCCOUNT_LIST_NOT_EXIST,
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": msg.ACCCOUNT_LIST_NOT_EXIST,
            "allow_registration": True,
        },
        {
            "class": AccListExists,
            "error_code": err.ACCCOUNT_LIST_EXISTS,
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": msg.ACCCOUNT_LIST_EXISTS,
            "allow_registration": True,
        },
    ],
    "account_products": [
        {
            "class": AccProductstNotExist,
            "error_code": err.ACCCOUNT_PRODUCTS_NOT_EXIST,
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": msg.ACCCOUNT_PRODUCTS_NOT_EXIST,
            "allow_registration": True,
        },
        {
            "class": AccProductsExists,
            "error_code": err.ACCCOUNT_PRODUCTS_EXISTS,
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": msg.ACCCOUNT_PRODUCTS_EXISTS,
            "allow_registration": True,
        },
    ],
    "accounts": [
        {
            "class": AccsNotExist,
            "error_code": err.ACCCOUNT_NOT_EXIST,
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": msg.ACCCOUNT_NOT_EXIST,
            "allow_registration": True,
        },
        {
            "class": AccsExists,
            "error_code": err.ACCCOUNT_EXISTS,
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": msg.ACCCOUNT_EXISTS,
            "allow_registration": True,
        },
    ],
    "addresses": [
        {
            "class": AddressNotExist,
            "error_code": err.ADDRESSES_NOT_EXIST,
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": msg.ADDRESSES_NOT_EXIST,
            "allow_registration": True,
        },
        {
            "class": AddressExists,
            "error_code": err.ADDRESSES_EXISTS,
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": msg.ACCCOUNT_EXISTS,
            "allow_registration": True,
        },
    ],
    "auth": [
        {
            "class": InvalidCredentials,
            "error_code": err.INVALID_CREDENTIALS,
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": msg.INVALID_CREDENTIALS,
            "allow_registration": True,
        },
    ],
    "emails": [
        {
            "class": EmailNotExist,
            "error_code": err.EMAIL_NOT_EXIST,
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": msg.EMAIL_NOT_EXIST,
            "allow_registration": True,
        },
        {
            "class": EmailExists,
            "error_code": err.EMAIL_EXISTS,
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": msg.EMAIL_EXISTS,
            "allow_registration": True,
        },
    ],
    "entities": [
        {
            "class": EntityNotExist,
            "error_code": err.ENTITY_NOT_EXIST,
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": msg.ENTITY_NOT_EXIST,
            "allow_registration": True,
        },
        {
            "class": EntityExists,
            "error_code": err.ENTITY_EXISTS,
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": msg.ENTITY_EXISTS,
            "allow_registration": True,
        },
        {
            "class": EntityIndivDataInvalid,
            "error_code": err.ENTITY_INDIV_DATA_INVALID,
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": msg.ENTITY_INDIV_DATA_INVALID,
            "allow_registration": True,
        },
        {
            "class": EntityNonIndivDataInvalid,
            "error_code": err.ENTITY_NON_INDIV_DATA_INVALID,
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": msg.ENTITY_NON_INDIV_DATA_INVALID,
            "allow_registration": True,
        },
        {
            "class": EntityDataInvalid,
            "error_code": err.ENTITY_DATA_INVALID,
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": msg.ENTITY_DATA_INVALID,
            "allow_registration": True,
        },
        {
            "class": EntityTypeInvalid,
            "error_code": err.ENTTIY_TYPE_INVALID,
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": msg.ENTITY_TYPE_INVALID,
            "allow_registration": True,
        },
    ],
    "entity_accounts": [
        {
            "class": EntityAccNotExist,
            "error_code": err.ENTITY_ACCOUNT_NOT_EXIST,
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": msg.ENTITY_ACCOUNT_NOT_EXIST,
            "allow_registration": True,
        },
        {
            "class": EntityAccExists,
            "error_code": err.ENTITY_ACCOUNT_EXISTS,
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": msg.ENTITY_ACCOUNT_EXISTS,
            "allow_registration": True,
        },
    ],
    "individuals": [
        {
            "class": IndividualNotExist,
            "error_code": err.INDIVIDUAL_NOT_EXIST,
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": msg.INDIVIDUAL_NOT_EXIST,
            "allow_registration": True,
        },
        {
            "class": IndividualExists,
            "error_code": err.INDIVIDUAL_EXISTS,
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": msg.INDIVIDUAL_EXISTS,
            "allow_registration": True,
        },
    ],
    "invoices": [
        {
            "class": InvoiceNotExist,
            "error_code": err.INVOICE_NOT_EXIST,
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": msg.INVOICE_NOT_EXIST,
            "allow_registration": True,
        },
        {
            "class": InvoiceExists,
            "error_code": err.INVOICE_EXISTS,
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": msg.INVOICE_EXISTS,
            "allow_registration": True,
        },
    ],
    "non_individuals": [
        {
            "class": NonIndividualNotExist,
            "error_code": err.NON_INDIVIDUAL_NOT_EXIST,
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": msg.NON_INDIVIDUAL_NOT_EXIST,
            "allow_registration": True,
        },
        {
            "class": NonIndividualExists,
            "error_code": err.NON_INDIVIDUAL_EXISTS,
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": msg.NON_INDIVIDUAL_EXISTS,
            "allow_registration": True,
        },
    ],
    "numbers": [
        {
            "class": NumbersNotExist,
            "error_code": err.NUMBER_NOT_EXIST,
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": msg.NUMBER_NOT_EXIST,
            "allow_registration": True,
        },
        {
            "class": NumberExists,
            "error_code": err.NUMBER_EXISTS,
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": msg.NUMBER_EXISTS,
            "allow_registration": True,
        },
    ],
    "order_items": [
        {
            "class": OrderItemNotExist,
            "error_code": err.ORDER_ITEM_NOT_EXIST,
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": msg.ORDER_ITEM_NOT_EXIST,
            "allow_registration": True,
        },
        {
            "class": OrderItemExists,
            "error_code": err.ORDER_ITEM_EXISTS,
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": msg.ORDER_ITEM_EXISTS,
            "allow_registration": True,
        },
    ],
    "orders": [
        {
            "class": OrderNotExist,
            "error_code": err.ORDER_NOT_EXIST,
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": msg.ORDER_NOT_EXIST,
            "allow_registration": True,
        },
        {
            "class": OrderExists,
            "error_code": err.ORDER_EXISTS,
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": msg.ORDER_EXISTS,
            "allow_registration": True,
        },
    ],
    "product_list_items": [
        {
            "class": ProductListItemNotExist,
            "error_code": err.PRODUCT_LIST_ITEM_NOT_EXIST,
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": msg.PRODUCT_LIST_ITEM_NOT_EXIST,
            "allow_registration": True,
        },
        {
            "class": ProductListItemExists,
            "error_code": err.PRODUCT_LIST_ITEM_EXISTS,
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": msg.PRODUCT_LIST_ITEM_EXISTS,
            "allow_registration": True,
        },
    ],
    "product_lists": [
        {
            "class": ProductListNotExist,
            "error_code": err.PRODUCT_LIST_NOT_EXIST,
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": msg.PRODUCT_LIST_NOT_EXIST,
            "allow_registration": True,
        },
        {
            "class": ProductListExists,
            "error_code": err.PRODUCT_LIST_EXISTS,
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": msg.PRODUCT_LIST_EXISTS,
            "allow_registration": True,
        },
    ],
    "products": [
        {
            "class": ProductsNotExist,
            "error_code": err.PRODUCT_NOT_EXIST,
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": msg.PRODUCT_NOT_EXIST,
            "allow_registration": True,
        },
        {
            "class": ProductsExists,
            "error_code": err.PRODUCT_EXISTS,
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": msg.PRODUCT_EXISTS,
            "allow_registration": True,
        },
    ],
    "sys_users": [
        {
            "class": SysUserNotExist,
            "error_code": err.SYS_USER_NOT_EXIST,
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": msg.SYS_USER_NOT_EXIST,
            "allow_registration": True,
        },
        {
            "class": SysUserExists,
            "error_code": err.SYS_USER_EXISTS,
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": msg.SYS_USER_EXISTS,
            "allow_registration": True,
        },
    ],
    "webistes": [
        {
            "class": WebsitesNotExist,
            "error_code": err.WEBSITE_NOT_EXIST,
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": msg.WEBSITE_NOT_EXIST,
            "allow_registration": True,
        },
        {
            "class": WebsitesExists,
            "error_code": err.WEBSITE_EXISTS,
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": msg.WEBSITE_EXISTS,
            "allow_registration": True,
        },
    ],
    "unhandled": [
        {
            "class": UnhandledException,
            "error_code": err.UNHANDLED_EXCEPTION,
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": msg.UNHANDLED_EXCEPTION,
            "allow_registration": True,
        },
    ],
}
