from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Callable

import app.schemas.account_contracts as schema

from ..constants import constants as cnst
from ..database.operations import Operations
from ..exceptions import AccContractNotExist
from ..models import AccountContracts

from ..statements.account_contracts import AccountContractStms
from ..utilities.utilities import DataUtils as di


class ReadSrvc:
    """
    Read service class for account contracts.

    This class provides methods for reading account contracts from the database.

    Expects an instance of a database connection to be passed in for each method.

    ivars:
    ivar: _statement: A instance of AccountContractStms.
    varType: AccountContractStms
    ivar: _db_ops: A utility class for database operations.
    varType: Operations
    """

    def __init__(
        self,
        statements: AccountContractStms,
        db_operations: Operations,
    ) -> None:
        """
        Initializes the ReadService class.

        :param statements: An instance of AccountContractStms.
        :type statements: AccountContractStms
        :param db_operations: A utility class for database operations.
        :type db_operations: Operations
        :return: None
        :rtype: None
        """
        self._statements = statements
        self._db_ops = db_operations

    async def get_account_contract(
        self,
        account_uuid: UUID4,
        account_contract_uuid: UUID4,
        db: AsyncSession,
    ) -> AccountContracts:
        """
        Fetches an account contract from the database.

        :param account_uuid: The UUID of the account.
        :type account_uuid: UUID4
        :param account_contract_uuid: The UUID of the account contract.
        :type account_contract_uuid: UUID4
        :param db: The database session.
        :type db: AsyncSession
        :return: The account contract.
        :rtype: AccountContracts
        :raises AccContractNotExist: If the account contract does not exist.
        """
        statement = self._statements.get_account_contract(
            account_uuid=account_uuid, account_contract_uuid=account_contract_uuid
        )

        account_contract = await self._db_ops.return_one_row(
            service=cnst.ACCOUNTS_CONTRACTS_READ_SERVICE, statement=statement, db=db
        )
        return di.record_not_exist(
            instance=account_contract, exception=AccContractNotExist
        )

    async def get_account_contracts(
        self,
        account_uuid: UUID4,
        limit: int,
        offset: int,
        db: AsyncSession,
    ) -> AccountContracts:
        """
        Fetches account contracts from the database by account.

        :param account_uuid: The UUID of the account.
        :type account_uuid: UUID4
        :param limit: The number of records to fetch.
        :type limit: int
        :param offset: The number of records to skip.
        :type offset: int
        :param db: The database session.
        :type db: AsyncSession
        :return: The account contracts.
        :rtype: AccountContracts
        :raises AccContractNotExist: If the account contracts do not exist.
        """

        statement = self._statements.get_account_contracts(
            account_uuid=account_uuid,
            limit=limit,
            offset=offset,
        )
        account_contracts = await self._db_ops.return_all_rows(
            service=cnst.ACCOUNTS_CONTRACTS_READ_SERVICE, statement=statement, db=db
        )
        return di.record_not_exist(
            instance=account_contracts, exception=AccContractNotExist
        )

    async def get_account_contracts_count(
        self,
        account_uuid: UUID4,
        db: AsyncSession,
    ) -> int:
        """
        Fetches the count of account contracts from the database by account.

        :param account_uuid: The UUID of the account.
        :type account_uuid: UUID4
        :param db: The database session.
        :type db: AsyncSession
        :return: The count of account contracts.
        :rtype: int
        :raises AccContractNotExist: If the account contracts do not exist.
        :raises RecordAlreadyExists: If the account contracts already exist.
        """
        statement = self._statements.account_contracts_count(account_uuid=account_uuid)
        return await self._db_ops.return_count(
            service=cnst.ACCOUNTS_CONTRACTS_READ_SERVICE, statement=statement, db=db
        )


class CreateSrvc:
    """
    Service class to create account contracts.

    Expects an instance of a database connection to be passed in for each method.

    ivars:
    ivar: _db_ops: A utility class for database operations.
    varType: Operations
    ivar: _account_contracts_model: The model for the account contract.
    varType: AccountContracts
    """

    def __init__(
        self,
        db_operations: Operations,
        model: AccountContracts,
    ) -> None:
        """
        Initializes the CreateService class.

        :param db_operations: A utility class for database operations.
        :type db_operations: Operations
        :param model: The model for the account contract.
        :type model: AccountContracts
        :return: None
        :rtype: None
        """
        self._db_ops: Operations = db_operations
        self._account_contracts_model: AccountContracts = model

    async def create_account_contract(
        self,
        account_uuid: UUID4,
        account_contract_data: schema.AccountContractsCreate,
        db: AsyncSession,
    ) -> AccountContracts:
        """
        Creates an account contract in the database.

        :param account_uuid: The UUID of the account.
        :type account_uuid: UUID4
        :param account_contract_data: The data for the account contract.
        :type account_contract_data: AccountContractsCreate
        :param db: The database session.
        :type db: AsyncSession
        :return: The created account contract.
        :rtype: AccountContracts
        :raises AccContractNotExist: If the account contract does not exist.
        """

        account_contract = await self._db_ops.add_instance(
            service=cnst.ACCOUNTS_CONTRACTS_CREATE_SERVICE,
            model=self._account_contracts_model,
            data=account_contract_data,
            db=db,
        )
        return di.record_not_exist(
            instance=account_contract, exception=AccContractNotExist
        )


class UpdateSrvc:
    """
    Update service class for account contracts.

    Expects an instance of a database connection to be passed in for each method.

    ivars:
    ivar: _statements: An instance of AccountContractStms.
    varType: AccountContractStms
    ivar: _db_ops: A utility class for database operations.
    varType: Operations
    """

    def __init__(
        self,
        statements: AccountContractStms,
        db_operations: Operations,
    ) -> None:
        """
        Initializes the UpdateService class.

        :param statement_factory: A factory function that returns an instance of AccountContractStms.
        :type statement_factory: Callable[[], AccountContractStms]
        :param db_operations: A utility class for database operations.
        :type db_operations: Operations
        :return: None
        :rtype: None
        """
        self._statements = statements
        self._db_ops = db_operations

    async def update_account_contract(
        self,
        account_uuid: UUID4,
        account_contract_uuid: UUID4,
        account_contract_data: schema.AccountContractsUpdate,
        db: AsyncSession,
    ) -> AccountContracts:
        """
        Updates an account contract in the database.

        :param account_uuid: The UUID of the account.
        :type account_uuid: UUID4
        :param account_contract_uuid: The UUID of the account contract.
        :type account_contract_uuid: UUID4
        :param account_contract_data: The data for the account contract.
        :type account_contract_data: AccountContractsUpdate
        :param db: The database session.
        :type db: AsyncSession
        :return: The updated account contract.
        :rtype: AccountContracts
        :raises AccContractNotExist: If the account contract does not exist.
        """
        statement = self._statements.update_account_contract(
            account_uuid=account_uuid,
            account_contract_uuid=account_contract_uuid,
            account_contract_data=account_contract_data,
        )
        account_contract = await self._db_ops.return_one_row(
            service=cnst.ACCOUNTS_CONTRACTS_UPDATE_SERVICE,
            statement=statement,
            db=db,
        )
        return di.record_not_exist(
            instance=account_contract, exception=AccContractNotExist
        )


class DeleteSrvc:
    """
    Delete service class for account contracts.

    Expects an instance of a database connection to be passed in for each method.

    ivars:
    ivar: _statements: An instance of AccountContractStms.
    varType: AccountContractStms
    ivar: _db_ops: A utility class for database operations.
    varType: Operations
    """

    def __init__(
        self,
        statements: AccountContractStms,
        db_operations: Operations,
    ) -> None:
        """
        Initializes the DeleteService class.

        :param statements: An instance of AccountContractStms.
        :type statements: AccountContractStms
        :param db_operations: A utility class for database operations.
        :type db_operations: Operations
        :return: None
        :rtype: None
        """
        self._statements = statements
        self._db_ops = db_operations

    async def soft_delete_account_contract(
        self,
        account_uuid: UUID4,
        account_contract_uuid: UUID4,
        account_contract_data: schema.AccountContractsDel,
        db: AsyncSession,
    ) -> AccountContracts:
        """
        Soft deletes an account contract in the database.

        :param account_uuid: The UUID of the account.
        :type account_uuid: UUID4
        :param account_contract_uuid: The UUID of the account contract.
        :type account_contract_uuid: UUID4
        :param account_contract_data: The data for the account contract.
        :type account_contract_data: AccountContractsDel
        :param db: The database session.
        :type db: AsyncSession
        :return: The deleted account contract.
        :rtype: AccountContracts
        :raises AccContractNotExist: If the account contract does not exist.
        """
        statement = self._statements.update_account_contract(
            account_uuid=account_uuid,
            account_contract_uuid=account_contract_uuid,
            account_contract_data=account_contract_data,
        )
        account_contract = await self._db_ops.return_one_row(
            service=cnst.ACCOUNTS_CONTRACTS_UPDATE_SERVICE,
            statement=statement,
            db=db,
        )
        return di.record_not_exist(
            instance=account_contract, exception=AccContractNotExist
        )


# Factory functions
def account_contract_read_srvc(
    statements: AccountContractStms, operations: Operations
) -> ReadSrvc:
    """
    Factory function to create an instance of ReadService.

    :param statements: An instance of AccountContractStms.
    :type statements: AccountContractStms
    :param operations: A utility class for database operations.
    :type operations: Operations
    :return: An instance of ReadService.
    :returnType: ReadService
    """
    return ReadSrvc(statements=statements, db_operations=operations)


def account_contract_create_srvc(
    operations: Operations, model: AccountContracts
) -> CreateSrvc:
    """
    Factory function to create an instance of CreateService.

    :param operations: A utility class for database operations.
    :type operations: Operations
    :return: An instance of CreateService.
    :rtype: CreateService
    """
    return CreateSrvc(db_operations=operations, model=model)


def account_contract_update_srvc(
    statements: AccountContractStms, operations: Operations
) -> UpdateSrvc:
    """
    Factory function to create an instance of UpdateService.

    :param statements: An instance of AccountContractStms.
    :type statements: AccountContractStms
    :param operations: A utility class for database operations.
    :type operations: Operations
    :return: An instance of UpdateService.
    :rtype: UpdateService
    """
    return UpdateSrvc(statements=statements, db_operations=operations)


def account_contract_delete_srvc(
    statements: AccountContractStms, operations: Operations
) -> DeleteSrvc:
    """
    Factory function to create an instance of DeleteService.

    :param statements: An instance of AccountContractStms.
    :type statements: AccountContractStms
    :param operations: A utility class for database operations.
    :type operations: Operations
    :return: An instance of DelService.
    :rtype: DelService
    """
    return DeleteSrvc(statements=statements, db_operations=operations)
