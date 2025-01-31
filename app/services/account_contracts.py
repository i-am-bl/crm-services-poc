from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from ..constants import constants as cnst
from ..database.operations import Operations
from ..exceptions import AccContractNotExist
from ..models import AccountContracts
from ..schemas.account_contracts import (
    AccountContractsDelRes,
    AccountContractsInternalCreate,
    AccountContractsInternalUpdate,
    AccountContractsRes,
    AccountContractsCreate,
    AccountContractsDel,
    AccountContractsUpdate,
    AccountContractsPgRes,
)
from ..statements.account_contracts import AccountContractStms
from ..utilities import pagination
from ..utilities.data import record_not_exist


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

        :param statements: AccountContractStms: An instance of AccountContractStms.
        :param db_operations: Operations: A utility class for database operations.
        :return: None: None
        """
        self._statements = statements
        self._db_ops = db_operations

    async def get_account_contract(
        self,
        account_uuid: UUID4,
        account_contract_uuid: UUID4,
        db: AsyncSession,
    ) -> AccountContractsRes:
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

        account_contract: AccountContractsRes = await self._db_ops.return_one_row(
            service=cnst.ACCOUNTS_CONTRACTS_READ_SERVICE, statement=statement, db=db
        )
        return record_not_exist(
            instance=account_contract, exception=AccContractNotExist
        )

    async def get_account_contracts(
        self,
        account_uuid: UUID4,
        limit: int,
        offset: int,
        db: AsyncSession,
    ) -> AccountContractsRes:
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
        account_contracts: AccountContractsRes = await self._db_ops.return_all_rows(
            service=cnst.ACCOUNTS_CONTRACTS_READ_SERVICE, statement=statement, db=db
        )
        return record_not_exist(
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

    async def paginated_account_contracts(
        self, account_uuid: UUID4, page: int, limit: int, db: AsyncSession
    ) -> AccountContractsPgRes:
        """
        Fetches a paginated list of account contracts for a specific account.

        This method is has a dependency on
        """
        offset = pagination.page_offset(page=page, limit=limit)
        total_count = await self.get_account_contracts_count(
            account_uuid=account_uuid, db=db
        )
        account_contracts = await self.get_account_contracts(
            account_uuid=account_uuid, limit=limit, offset=offset, db=db
        )
        has_more = pagination.has_more_items(
            total_count=total_count, page=page, limit=limit
        )
        return AccountContractsPgRes(
            total=total_count,
            page=page,
            limit=limit,
            has_more=has_more,
            account_contracts=account_contracts,
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
        account_contract_data: AccountContractsInternalCreate,
        db: AsyncSession,
    ) -> AccountContractsRes:
        """
        Creates an account contract in the database.

        :param account_uuid: The UUID of the account.
        :type account_uuid: UUID4
        :param account_contract_data: The data for the account contract.
        :type account_contract_data: AccountContractsInternalCreate
        :param db: The database session.
        :type db: AsyncSession
        :return: The created account contract.
        :rtype: AccountContracts
        :raises AccContractNotExist: If the account contract does not exist.
        """

        account_contract: AccountContractsRes = await self._db_ops.add_instance(
            service=cnst.ACCOUNTS_CONTRACTS_CREATE_SERVICE,
            model=self._account_contracts_model,
            data=account_contract_data,
            db=db,
        )
        return record_not_exist(
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
        account_contract_data: AccountContractsInternalUpdate,
        db: AsyncSession,
    ) -> AccountContractsRes:
        """
        Updates an account contract in the database.

        :param account_uuid: The UUID of the account.
        :type account_uuid: UUID4
        :param account_contract_uuid: The UUID of the account contract.
        :type account_contract_uuid: UUID4
        :param account_contract_data: The data for the account contract.
        :type account_contract_data: AccountContractsInternalUpdate
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
        account_contract: AccountContractsRes = await self._db_ops.return_one_row(
            service=cnst.ACCOUNTS_CONTRACTS_UPDATE_SERVICE,
            statement=statement,
            db=db,
        )
        return record_not_exist(
            instance=account_contract, exception=AccContractNotExist
        )


class DelSrvc:
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
        account_contract_data: AccountContractsDel,
        db: AsyncSession,
    ) -> AccountContractsDelRes:
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
        account_contract: AccountContractsDelRes = await self._db_ops.return_one_row(
            service=cnst.ACCOUNTS_CONTRACTS_UPDATE_SERVICE,
            statement=statement,
            db=db,
        )
        return record_not_exist(
            instance=account_contract, exception=AccContractNotExist
        )
