"""  
Constant file for all messages set throughout this application.
"""

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
