from fastapi import status

from .constants import error_codes as err
from .constants import messages as msg
from .exceptions import *
from .handlers import *


def register_exception_handlers(app):

    # Account Contracts
    app.add_exception_handler(
        exc_class_or_status_code=AccContractNotExist,
        handler=create_exception_handler(
            error_code=err.ACCCOUNT_CONTRACT_NOT_EXIST,
            status_code=status.HTTP_400_BAD_REQUEST,
            message=msg.ACCCOUNT_CONTRACT_NOT_EXIST,
        ),
    )
    app.add_exception_handler(
        exc_class_or_status_code=AccContractExists,
        handler=create_exception_handler(
            error_code=err.ACCCOUNT_CONTRACT_EXISTS,
            status_code=status.HTTP_400_BAD_REQUEST,
            message=msg.ACCCOUNT_CONTRACT_EXISTS,
        ),
    )

    # Accounts Lists
    app.add_exception_handler(
        exc_class_or_status_code=AccListNotExist,
        handler=create_exception_handler(
            error_code=err.ACCCOUNT_LIST_NOT_EXIST,
            status_code=status.HTTP_400_BAD_REQUEST,
            message=msg.ACCCOUNT_LIST_NOT_EXIST,
        ),
    )
    app.add_exception_handler(
        exc_class_or_status_code=AccListExists,
        handler=create_exception_handler(
            error_code=err.ACCCOUNT_LIST_EXISTS,
            status_code=status.HTTP_400_BAD_REQUEST,
            message=msg.ACCCOUNT_LIST_EXISTS,
        ),
    )

    # Accounts Products
    app.add_exception_handler(
        exc_class_or_status_code=AccProductstNotExist,
        handler=create_exception_handler(
            error_code=err.ACCCOUNT_PRODUCTS_NOT_EXIST,
            status_code=status.HTTP_400_BAD_REQUEST,
            message=msg.ACCCOUNT_PRODUCTS_NOT_EXIST,
        ),
    )
    app.add_exception_handler(
        exc_class_or_status_code=AccProductsExists,
        handler=create_exception_handler(
            error_code=err.ACCCOUNT_PRODUCTS_EXISTS,
            status_code=status.HTTP_400_BAD_REQUEST,
            message=msg.ACCCOUNT_PRODUCTS_EXISTS,
        ),
    )

    # Accounts
    app.add_exception_handler(
        exc_class_or_status_code=AccsNotExist,
        handler=create_exception_handler(
            error_code=err.ACCCOUNT_NOT_EXIST,
            status_code=status.HTTP_400_BAD_REQUEST,
            message=msg.ACCCOUNT_NOT_EXIST,
        ),
    )
    app.add_exception_handler(
        exc_class_or_status_code=AccsExists,
        handler=create_exception_handler(
            error_code=err.ACCCOUNT_EXISTS,
            status_code=status.HTTP_400_BAD_REQUEST,
            message=msg.ACCCOUNT_EXISTS,
        ),
    )

    # Auth
    app.add_exception_handler(
        exc_class_or_status_code=InvalidCredentials,
        handler=create_exception_handler(
            error_code=err.INVALID_CREDENTIALS,
            status_code=status.HTTP_400_BAD_REQUEST,
            message=msg.INVALID_CREDENTIALS,
        ),
    )

    # Emails
    app.add_exception_handler(
        exc_class_or_status_code=EmailNotExist,
        handler=create_exception_handler(
            error_code=err.EMAIL_NOT_EXIST,
            status_code=status.HTTP_400_BAD_REQUEST,
            message=msg.EMAIL_NOT_EXIST,
        ),
    )
    app.add_exception_handler(
        exc_class_or_status_code=EmailExists,
        handler=create_exception_handler(
            error_code=err.EMAIL_EXISTS,
            status_code=status.HTTP_400_BAD_REQUEST,
            message=msg.EMAIL_EXISTS,
        ),
    )

    # Entities
    app.add_exception_handler(
        exc_class_or_status_code=EntityNotExist,
        handler=create_exception_handler(
            error_code=err.ENTITY_NOT_EXIST,
            status_code=status.HTTP_400_BAD_REQUEST,
            message=msg.ENTITY_NOT_EXIST,
        ),
    )
    app.add_exception_handler(
        exc_class_or_status_code=EntityExists,
        handler=create_exception_handler(
            error_code=err.ENTITY_EXISTS,
            status_code=status.HTTP_400_BAD_REQUEST,
            message=msg.ENTITY_EXISTS,
        ),
    )

    # Entity Accounts
    app.add_exception_handler(
        exc_class_or_status_code=EntityAccNotExist,
        handler=create_exception_handler(
            error_code=err.ENTITY_ACCOUNT_NOT_EXIST,
            status_code=status.HTTP_400_BAD_REQUEST,
            message=msg.ENTITY_ACCOUNT_NOT_EXIST,
        ),
    )
    app.add_exception_handler(
        exc_class_or_status_code=EntityAccExists,
        handler=create_exception_handler(
            error_code=err.ENTITY_ACCOUNT_EXISTS,
            status_code=status.HTTP_400_BAD_REQUEST,
            message=msg.ENTITY_ACCOUNT_EXISTS,
        ),
    )

    # Individuals
    app.add_exception_handler(
        exc_class_or_status_code=IndividualNotExist,
        handler=create_exception_handler(
            error_code=err.INDIVIDUAL_NOT_EXIST,
            status_code=status.HTTP_400_BAD_REQUEST,
            message=msg.INDIVIDUAL_NOT_EXIST,
        ),
    )
    app.add_exception_handler(
        exc_class_or_status_code=IndividualExists,
        handler=create_exception_handler(
            error_code=err.INDIVIDUAL_EXISTS,
            status_code=status.HTTP_400_BAD_REQUEST,
            message=msg.INDIVIDUAL_EXISTS,
        ),
    )

    # Invoice Items
    app.add_exception_handler(
        exc_class_or_status_code=InvoiceItemNotExist,
        handler=create_exception_handler(
            error_code=err.INVOICE_ITEM_NOT_EXIST,
            status_code=status.HTTP_400_BAD_REQUEST,
            message=msg.INVOICE_ITEM_NOT_EXIST,
        ),
    )
    app.add_exception_handler(
        exc_class_or_status_code=InvoiceItemExists,
        handler=create_exception_handler(
            error_code=err.INVOICE_ITEM_EXISTS,
            status_code=status.HTTP_400_BAD_REQUEST,
            message=msg.INVOICE_ITEM_EXISTS,
        ),
    )

    # Invoices
    app.add_exception_handler(
        exc_class_or_status_code=InvoiceNotExist,
        handler=create_exception_handler(
            error_code=err.INVOICE_NOT_EXIST,
            status_code=status.HTTP_400_BAD_REQUEST,
            message=msg.INVOICE_NOT_EXIST,
        ),
    )
    app.add_exception_handler(
        exc_class_or_status_code=InvoiceExists,
        handler=create_exception_handler(
            error_code=err.INVOICE_EXISTS,
            status_code=status.HTTP_400_BAD_REQUEST,
            message=msg.INVOICE_EXISTS,
        ),
    )

    # Non-individuals
    app.add_exception_handler(
        exc_class_or_status_code=NonIndividualNotExist,
        handler=create_exception_handler(
            error_code=err.NON_INDIVIDUAL_NOT_EXIST,
            status_code=status.HTTP_400_BAD_REQUEST,
            message=msg.NON_INDIVIDUAL_NOT_EXIST,
        ),
    )
    app.add_exception_handler(
        exc_class_or_status_code=NonIndividualExists,
        handler=create_exception_handler(
            error_code=err.NON_INDIVIDUAL_EXISTS,
            status_code=status.HTTP_400_BAD_REQUEST,
            message=msg.NON_INDIVIDUAL_EXISTS,
        ),
    )

    # Numbers
    app.add_exception_handler(
        exc_class_or_status_code=NumbersNotExist,
        handler=create_exception_handler(
            error_code=err.NUMBER_NOT_EXIST,
            status_code=status.HTTP_400_BAD_REQUEST,
            message=msg.NUMBER_NOT_EXIST,
        ),
    )
    app.add_exception_handler(
        exc_class_or_status_code=NumberExists,
        handler=create_exception_handler(
            error_code=err.NUMBER_EXISTS,
            status_code=status.HTTP_400_BAD_REQUEST,
            message=msg.NUMBER_EXISTS,
        ),
    )

    # Order Items
    app.add_exception_handler(
        exc_class_or_status_code=OrderItemNotExist,
        handler=create_exception_handler(
            error_code=err.ORDER_ITEM_NOT_EXIST,
            status_code=status.HTTP_400_BAD_REQUEST,
            message=msg.ORDER_ITEM_NOT_EXIST,
        ),
    )
    app.add_exception_handler(
        exc_class_or_status_code=OrderItemExists,
        handler=create_exception_handler(
            error_code=err.ORDER_ITEM_EXISTS,
            status_code=status.HTTP_400_BAD_REQUEST,
            message=msg.ORDER_ITEM_EXISTS,
        ),
    )

    # Orders
    app.add_exception_handler(
        exc_class_or_status_code=OrderNotExist,
        handler=create_exception_handler(
            error_code=err.ORDER_NOT_EXIST,
            status_code=status.HTTP_400_BAD_REQUEST,
            message=msg.ORDER_NOT_EXIST,
        ),
    )
    app.add_exception_handler(
        exc_class_or_status_code=OrderExists,
        handler=create_exception_handler(
            error_code=err.ORDER_EXISTS,
            status_code=status.HTTP_400_BAD_REQUEST,
            message=msg.ORDER_EXISTS,
        ),
    )

    # Product List Items
    app.add_exception_handler(
        exc_class_or_status_code=ProductListItemNotExist,
        handler=create_exception_handler(
            error_code=err.PRODUCT_LIST_ITEM_NOT_EXIST,
            status_code=status.HTTP_400_BAD_REQUEST,
            message=msg.PRODUCT_LIST_ITEM_NOT_EXIST,
        ),
    )
    app.add_exception_handler(
        exc_class_or_status_code=ProductListItemExists,
        handler=create_exception_handler(
            error_code=err.PRODUCT_LIST_ITEM_EXISTS,
            status_code=status.HTTP_400_BAD_REQUEST,
            message=msg.PRODUCT_LIST_ITEM_EXISTS,
        ),
    )

    # Product Lists
    app.add_exception_handler(
        exc_class_or_status_code=ProductListNotExist,
        handler=create_exception_handler(
            error_code=err.PRODUCT_LIST_NOT_EXIST,
            status_code=status.HTTP_400_BAD_REQUEST,
            message=msg.PRODUCT_LIST_NOT_EXIST,
        ),
    )
    app.add_exception_handler(
        exc_class_or_status_code=ProductListExists,
        handler=create_exception_handler(
            error_code=err.PRODUCT_LIST_EXISTS,
            status_code=status.HTTP_400_BAD_REQUEST,
            message=msg.PRODUCT_LIST_EXISTS,
        ),
    )

    # Products
    app.add_exception_handler(
        exc_class_or_status_code=ProductsNotExist,
        handler=create_exception_handler(
            error_code=err.PRODUCT_NOT_EXIST,
            status_code=status.HTTP_400_BAD_REQUEST,
            message=msg.PRODUCT_NOT_EXIST,
        ),
    )
    app.add_exception_handler(
        exc_class_or_status_code=ProductsExists,
        handler=create_exception_handler(
            error_code=err.PRODUCT_EXISTS,
            status_code=status.HTTP_400_BAD_REQUEST,
            message=msg.PRODUCT_EXISTS,
        ),
    )

    # SysUsers
    app.add_exception_handler(
        exc_class_or_status_code=SysUserNotExist,
        handler=create_exception_handler(
            error_code=err.SYS_USER_NOT_EXIST,
            status_code=status.HTTP_400_BAD_REQUEST,
            message=msg.SYS_USER_NOT_EXIST,
        ),
    )
    app.add_exception_handler(
        exc_class_or_status_code=SysUserExists,
        handler=create_exception_handler(
            error_code=err.SYS_USER_EXISTS,
            status_code=status.HTTP_400_BAD_REQUEST,
            message=msg.SYS_USER_NOT_EXIST,
        ),
    )

    # Websites
    app.add_exception_handler(
        exc_class_or_status_code=WebsitesNotExist,
        handler=create_exception_handler(
            error_code=err.WEBSITE_NOT_EXIST,
            status_code=status.HTTP_400_BAD_REQUEST,
            message=msg.WEBSITE_NOT_EXIST,
        ),
    )
    app.add_exception_handler(
        exc_class_or_status_code=WebsitesExists,
        handler=create_exception_handler(
            error_code=err.WEBSITE_EXISTS,
            status_code=status.HTTP_400_BAD_REQUEST,
            message=msg.WEBSITE_EXISTS,
        ),
    )

    # Unhandled
    app.add_exception_handler(
        exc_class_or_status_code=UnhandledException,
        handler=create_exception_handler(
            error_code=err.UNHANDLED_EXCEPTION,
            status_code=status.HTTP_400_BAD_REQUEST,
            message=msg.UNHANDLED_EXCEPTION,
        ),
    )
