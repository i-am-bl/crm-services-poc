"""
The exceptions package contains multiple modules, each defining custom exception classes. 
These exception classes inherit from the base class CRMExceptions, which in turn inherits from 
Python's built-in Exception class. Each custom exception class is associated with a default message 
and provides logging capabilities, ensuring better error handling and traceability across the application.
"""

from .account_contracts import *
from .account_lists import *
from .account_products import *
from .accounts import *
from .addresses import *
from .authentication import *
from .emails import *
from .entities import *
from .entity_accounts import *
from .general import *
from .individuals import *
from .invoice_items import *
from .invoices import *
from .non_individuals import *
from .numbers import *
from .order_items import *
from .orders import *
from .product_list_items import *
from .product_lists import *
from .products import *
from .sys_users import *
from .websites import *
