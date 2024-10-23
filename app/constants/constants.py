"""  
Global constants set throughout this application.
"""

ACC_TRNS_TYPE_CREATE = "create"
ACC_TRNS_TYPE_VAL_CREATE = "validate_then_create"

ACCOUNTS_CREATE_SERVICE = "AccountsCreateService"
ACCOUNTS_DEL_SERVICE = "AccountsDelService"
ACCOUNTS_READ_SERVICE = "AccountsReadService"
ACCOUNTS_UPDATE_SERVICE = "AccountsUpdateService"

ACCOUNTS_CONTRACTS_CREATE_SERVICE = "AccountContractsCreateService"
ACCOUNTS_CONTRACTS_DEL_SERVICE = "AccountContractsDelService"
ACCOUNTS_CONTRACTS_READ_SERVICE = "AccountContractsReadService"
ACCOUNTS_CONTRACTS_UPDATE_SERVICE = "AccountContractsUpdateService"

ACCOUNTS_LISTS_CREATE_SERVICE = "AccountListsCreateService"
ACCOUNTS_LISTS_DEL_SERVICE = "AccountListsDelService"
ACCOUNTS_LISTS_READ_SERVICE = "AccountListsReadService"
ACCOUNTS_LISTS_UPDATE_SERVICE = "AccountListsUpdateService"

ACCOUNTS_PRODUCTS_CREATE_SERVICE = "AccountProductsCreateService"
ACCOUNTS_PRODUCTS_DEL_SERVICE = "AccountProductsDelService"
ACCOUNTS_PRODUCTS_READ_SERVICE = "AccountProductsReadService"
ACCOUNTS_PRODUCTS_UPDATE_SERVICE = "AccountProductsUpdateService"

ADDRESSES_CREATE_SERVICE = "AddressesCreateService"
ADDRESSES_DEL_SERVICE = "AddressesDelService"
ADDRESSES_READ_SERVICE = "AddressesReadService"
ADDRESSES_UPDATE_SERVICE = "AddressesUpdateService"

AUTH_SERVICE = "AuthService"

DOLLAR = "dollar"

EMAILS_CREATE_SERVICE = "EmailsCreateService"
EMAILS_DEL_SERVICE = "EmailsDelService"
EMAILS_READ_SERVICE = "EmailsReadService"
EMAILS_UPDATE_SERVICE = "EmailsUpdateService"

ENTITIES_CREATE_SERV = "EntitiesCreateService"
ENTITIES_DEL_SERV = "EntitiesDelService"
ENTITIES_READ_SERV = "EntitiesReadService"
ENTITIES_UPDATE_SERV = "EntitiesUpdateService"

ENTITY_ACCOUNTS_CREATE_SERV = "EntityAccountsCreateService"
ENTITY_ACCOUNTS_DEL_SERV = "EntityAccountsDelService"
ENTITY_ACCOUNTS_READ_SERV = "EntityAccountsReadService"
ENTITY_ACCOUNTS_UPDATE_SERV = "EntityAccountsUpdateService"

ENTITY_EMAIL = "email"
ENTITY_INDIVIDUAL = "individual"
ENTITY_NON_INDIVIDUAL = "non-individual"
ENTITY_PARENT = "entity"
ENTITY_UUID = "uuid"

INDIVIDUALS_CREATE_SERV = "IndividualsCreateService"
INDIVIDUALS_DEL_SERV = "IndividualsDelService"
INDIVIDUALS_READ_SERV = "IndividualsReadService"
INDIVIDUALS_UPDATE_SERV = "IndividualsUpdateService"

INVOICE_ITEMS_CREATE_SERV = "InvoiceItemsCreateService"
INVOICE_ITEMS_DEL_SERV = "InvoiceItemsDelService"
INVOICE_ITEMS_READ_SERV = "InvoiceItemsReadService"
INVOICE_ITEMS_UPDATE_SERV = "InvoiceItemsUpdateService"

INVOICES_CREATE_SERV = "InvoicesCreateService"
INVOICES_DEL_SERV = "InvoicesDelService"
INVOICES_READ_SERV = "InvoicesReadService"
INVOICES_UPDATE_SERV = "InvoicesUpdateService"

NON_INDIVIDUALS_CREATE_SERV = "NonIndividualsCreateService"
NON_INDIVIDUALS_DEL_SERV = "NonIndividualsDelService"
NON_INDIVIDUALS_READ_SERV = "NonIndividualsReadService"
NON_INDIVIDUALS_UPDATE_SERV = "NonIndividualsUpdateService"

NUMBER_QUERY_NUM = "entity_num_num"
NUMBER_QUERY_UUID = "entity_num_uuid"

NUMBERS_CREATE_SERVICE = "NumbersCreateService"
NUMBERS_DEL_SERVICE = "NumbersDelService"
NUMBERS_READ_SERVICE = "NumbersReadService"
NUMBERS_UPDATE_SERVICE = "NumbersUpdateService"

ORDERS_ITEMS_CREATE_SERVICE = "OrdersItemsCreateService"
ORDERS_ITEMS_DEL_SERVICE = "OrdersItemsDelService"
ORDERS_ITEMS_READ_SERVICE = "OrdersItemsReadService"
ORDERS_ITEMS_UPDATE_SERVICE = "OrdersItemsUpdateService"

ORDERS_CREATE_SERVICE = "OrdersCreateService"
ORDERS_DEL_SERVICE = "OrdersDelService"
ORDERS_READ_SERVICE = "OrdersReadService"
ORDERS_UPDATE_SERVICE = "OrdersUpdateService"

PERCENTAGE = "percentage"

PRODUCT_LIST_ITEMS_CREATE_SERV = "ProductListItemsCreateService"
PRODUCT_LIST_ITEMS_DEL_SERV = "ProductListItemsDelService"
PRODUCT_LIST_ITEMS_READ_SERV = "ProductListItemsReadService"
PRODUCT_LIST_ITEMS_UPDATE_SERV = "ProductListItemsUpdateService"

PRODUCT_LISTS_CREATE_SERV = "ProductListsCreateService"
PRODUCT_LISTS_DEL_SERV = "ProductListsDelService"
PRODUCT_LISTS_READ_SERV = "ProductListsReadService"
PRODUCT_LISTS_UPDATE_SERV = "ProductListsUpdateService"

PRODUCTS_CREATE_SERV = "ProductsCreateService"
PRODUCTS_DEL_SERV = "ProductsDelService"
PRODUCTS_READ_SERV = "ProductsReadService"
PRODUCTS_UPDATE_SERV = "ProductsUpdateService"

TAG_ACCOUNT_ADDRESSES = "Account-Addresses"
TAG_ACCOUNT_CONTRACTS = "Account-Contracts"
TAG_ACCOUNT_ENTITIES = "Account-Entities"
TAG_ACCOUNT_LISTS = "Account-Lists"
TAG_ACCOUNT_PRODUCTS = "Account-Products"
TAG_ACCOUNTS = "Accounts"
TAG_ENTITIES = "Entities"
TAG_SYS_USER = "Users"
TAG_ENTITY_ACCOUNTS = "Entity-Accounts"
TAG_ENTITY_ADDRESSES = "Entity-Addresses"
TAG_ENTITY_EMAILS = "Entity-Emails"
TAG_ENTITY_MANAGEMENT = "Entity-Management"
TAG_ENTITY_NUMBERS = "Entity-Numbers"
TAG_ENTITY_WEBSITES = "Entity-Websites"
TAG_INDIVIDUAL = "Individual"
TAG_INVOICE_ITEMS = "Invoice-Items"
TAG_INVOICES = "Invoices"
TAG_LOGIN = "Login"
TAG_NON_INDIVIDUAL = "Non-Individual"
TAG_ORDERS_ITEMS = "Order-Items"
TAG_ORDERS = "Orders"
TAG_PRODUCT_LIST_ITEMS = "Product-List-items"
TAG_PRODUCT_LISTS = "Product-Lists"
TAG_PRODUCTS = "Products"
TAG_SIGN_UP = "Sign-up"
TAG_ENTITY_MANAGEMENT = "Entity-Management"


TOKEN_TYPE = "bearer"
TOKEN_KEY = "jwt"
TOKEN_URL = "/v1/system-management/login/"

SCHEMAS = ["sales"]

SYS_USER_CREATE_SERV = "SysUserCreateService"
SYS_USER_DEL_SERV = "SysUserDelService"
SYS_USER_READ_SERV = "SysUserReadService"
SYS_USER_UPDATE_SERV = "SysUserUpdateService"

USER_USERNAME = "username"

WEBSITES_CREATE_SERVICE = "WebsitesCreateService"
WEBSITES_DEL_SERVICE = "WebsitesDelService"
WEBSITES_READ_SERVICE = "WebsitesReadService"
WEBSITES_UPDATE_SERVICE = "WebsitesUpdateService"

WEBSITE_QUERY_NAME = "entity_website_name"
WEBSITE_QUERY_UUID = "entity_website_uuid"

# variables for messages
_RECORD_EXISTS = "record already exists. A duplicate record is not allowed."
_RECORD_NOT_EXIST = "record does not exist."
