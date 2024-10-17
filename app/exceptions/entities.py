from app.exceptions.crm_exceptions import CRMExceptions


class EntityNotExist(CRMExceptions):
    pass


class EntityExists(CRMExceptions):
    pass
