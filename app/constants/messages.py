from .constants import _RECORD_EXISTS, _RECORD_NOT_EXIST

ACCCOUNT_CONTRACT_NOT_EXIST = f"Account contract {_RECORD_NOT_EXIST}"
ACCCOUNT_CONTRACT_EXISTS = f"Account contract {_RECORD_EXISTS}"

ACCCOUNT_LIST_NOT_EXIST = f"Account list {_RECORD_NOT_EXIST}"
ACCCOUNT_LIST_EXISTS = f"Account list {_RECORD_EXISTS}"

ACCCOUNT_PRODUCTS_NOT_EXIST = f"Account product {_RECORD_NOT_EXIST}"
ACCCOUNT_PRODUCTS_EXISTS = f"Account product {_RECORD_EXISTS}"

ACCCOUNT_NOT_EXIST = f"Account {_RECORD_NOT_EXIST}"
ACCCOUNT_EXISTS = f"Account {_RECORD_EXISTS}"

ADDRESSES_NOT_EXIST = f"Address {_RECORD_NOT_EXIST}"
ADDRESSES_EXISTS = f"Address {_RECORD_EXISTS}"

EMAIL_NOT_EXIST = f"Email {_RECORD_NOT_EXIST}"
EMAIL_EXISTS = f"Email {_RECORD_EXISTS}"

ENTITY_ACCOUNT_NOT_EXIST = f"Entity account {_RECORD_NOT_EXIST}"
ENTITY_ACCOUNT_EXISTS = f"Entity account {_RECORD_EXISTS}"

ENTITY_NOT_EXIST = f"Entity {_RECORD_NOT_EXIST}"
ENTITY_EXISTS = f"Entity {_RECORD_EXISTS}"

ENTITY_DATA_INVALID = "Entity data is invalid, a valid payload must be provided."

ENTITY_INDIV_DATA_INVALID = (
    "Individual data payload is invalid for entity_type: individual."
)
ENTITY_NON_INDIV_DATA_INVALID = (
    "Non-Individual data payload is invalid for entity_type: non-individual."
)

ENTITY_TYPE_INVALID = "entity_type is invalid."

INDIVIDUAL_NOT_EXIST = f"Individual {_RECORD_NOT_EXIST}"
INDIVIDUAL_EXISTS = f"Individual {_RECORD_EXISTS}"

INVALID_CREDENTIALS = "Invalid credentials."

INVOICE_ITEM_NOT_EXIST = f"Invoice item {_RECORD_NOT_EXIST}"
INVOICE_ITEM_EXISTS = f"Invoice item {_RECORD_EXISTS}"

INVOICE_NOT_EXIST = f"Invoice {_RECORD_NOT_EXIST}"
INVOICE_EXISTS = f"Invoice {_RECORD_EXISTS}"

NON_INDIVIDUAL_NOT_EXIST = f"Non-Individual {_RECORD_NOT_EXIST}"
NON_INDIVIDUAL_EXISTS = f"Non-Individual {_RECORD_EXISTS}"

NUMBER_NOT_EXIST = f"Number {_RECORD_NOT_EXIST}"
NUMBER_EXISTS = f"Number {_RECORD_EXISTS}"

ORDER_ITEM_NOT_EXIST = f"Order item {_RECORD_NOT_EXIST}"
ORDER_ITEM_EXISTS = f"Order item {_RECORD_EXISTS}"

ORDER_NOT_EXIST = f"Order {_RECORD_NOT_EXIST}"
ORDER_EXISTS = f"Order {_RECORD_EXISTS}"

PRODUCT_LIST_ITEM_NOT_EXIST = f"Product list item {_RECORD_NOT_EXIST}"
PRODUCT_LIST_ITEM_EXISTS = f"Product list item {_RECORD_EXISTS}"

PRODUCT_LIST_NOT_EXIST = f"Product list {_RECORD_NOT_EXIST}"
PRODUCT_LIST_EXISTS = f"Product list {_RECORD_EXISTS}"

PRODUCT_NOT_EXIST = f"Product {_RECORD_NOT_EXIST}"
PRODUCT_EXISTS = f"Product {_RECORD_EXISTS}"

SYS_USER_NOT_EXIST = f"Sys user {_RECORD_NOT_EXIST}"
SYS_USER_EXISTS = f"Sys user credential combination invalid."

TOKEN_REFRESH = "A new token was issued."

WEBSITE_NOT_EXIST = f"Website {_RECORD_NOT_EXIST}"
WEBSITE_EXISTS = f"Website {_RECORD_EXISTS}"

# Unhandled errors
UNHANDLED_EXCEPTION = "Something unexepected has occurred."


ERROR_DATABASE_EMPTY_TRANSACTION = "There is nothing to commit."
ERROR_DATABASE_TRANSACTION = "Transaction could not be committed."
ERORR_EMAIL_NOT_CREATED = "Unknown error occured, email was not created."
ERROR_EMAIL_EXISTS = "Email already exists for this entity and cannot be duplicated."
ERROR_EAMIL_NOT_EXIST = "Email does not exist for this entity."
ERROR_ENTITY_RECORD_NOT_FOUND = "There was no results returned for the {uuid} provided, please ensure the right type: {type} has been provided."
ERROR_ENTITY_PAYLOAD_MISSING = "Entity must include either an individual or non-indiviudal minimum required information."
ERROR_ENTITY_PAYLOAD_OVERLOADED = (
    "Entity can only be an individual or non-individual, not both."
)
ERROR_ENTITY_PAYLOAD_NOT_VALID = (
    "Entity type does not match the allowed entity information provided"
)
ERROR_UKNOWN_ERROR = (
    "Something unexpected happened, the request could not be completed."
)
ERROR_UPDATE_FAILED = "Update could not be made."
RECORD_EXISTS = "Record already exists, a duplicate entry is not allowed."
RECORD_NOT_EXIST = "Record does not exist."
SOFT_DELETED_RECORD = (
    "Record has been removed, contact your administrator to retrieve deleted record."
)
USER_DISABLED = "User has been disabled, please contact your administrator."
USER_EXISTS = "User could not be created."
USER_INVALID_CREDENTIALS = "Email or password is not valid."
USER_NOT_FOUND = "User not found."
