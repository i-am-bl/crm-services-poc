from typing import List

from pydantic import UUID4
from sqlalchemy import Select, update
from sqlalchemy.ext.asyncio import AsyncSession

from ..constants import constants as cnst
from ..database.operations import Operations
from ..exceptions import EmailExists, EmailNotExist
from ..models.emails import Emails
from ..schemas.emails import (
    EmailsCreate,
    EmailsUpdate,
    EmailsRes,
    EmailsDel,
    EmailsDelRes,
    EmailsPgRes,
)
from ..statements.emails import EmailsStms
from ..utilities import pagination
from ..utilities.data import record_not_exist, record_exists


class ReadSrvc:
    """
    Service for reading emails from the database.

    This class provides functionality to retrieve email data, either a single email or a list of emails, along with pagination support.

    :param statements: The SQL statements used for reading email data.
    :type statements: EmailsStms
    :param db_operations: The database operations object used for executing queries.
    :type db_operations: Operations
    """

    def __init__(self, statements: EmailsStms, db_operations: Operations) -> None:
        """
        Initializes the ReadSrvc class with the provided statements and database operations.

        :param statements: The SQL statements used for reading email data.
        :type statements: EmailsStms
        :param db_operations: The database operations object used for executing queries.
        :type db_operations: Operations
        """
        self._statements: EmailsStms = statements
        self._db_ops: Operations = db_operations

    @property
    def statements(self) -> EmailsStms:
        """
        Returns the email-related SQL statements.

        :return: The email-related SQL statements.
        :rtype: EmailsStms
        """
        return self._statements

    @property
    def db_operations(self) -> Operations:
        """
        Returns the database operations object.

        :return: The database operations object.
        :rtype: Operations
        """
        return self._db_ops

    async def get_email(
        self,
        entity_uuid: UUID4,
        email_uuid: UUID4,
        db: AsyncSession,
    ) -> EmailsRes:
        """
        Retrieves a single email by its UUID and the entity's UUID.

        :param entity_uuid: The UUID of the entity to which the email belongs.
        :type entity_uuid: UUID4
        :param email_uuid: The UUID of the email to retrieve.
        :type email_uuid: UUID4
        :param db: The database session.
        :type db: AsyncSession
        :return: The retrieved email data.
        :rtype: EmailsRes
        :raises EmailNotExist: If the email does not exist.
        """
        statement: Select = self._statements.get_email(
            entity_uuid=entity_uuid, email_uuid=email_uuid
        )
        email: EmailsRes = await self._db_ops.return_one_row(
            service=cnst.EMAILS_READ_SERVICE, statement=statement, db=db
        )
        return record_not_exist(instance=email, exception=EmailNotExist)

    async def get_emails(
        self,
        entity_uuid: UUID4,
        limit: int,
        offset: int,
        db: AsyncSession,
    ) -> List[EmailsRes]:
        """
        Retrieves a list of emails associated with a given entity UUID, paginated by limit and offset.

        :param entity_uuid: The UUID of the entity to which the emails belong.
        :type entity_uuid: UUID4
        :param limit: The maximum number of emails to retrieve.
        :type limit: int
        :param offset: The offset for pagination.
        :type offset: int
        :param db: The database session.
        :type db: AsyncSession
        :return: The list of emails.
        :rtype: List[EmailsRes]
        :raises EmailNotExist: If no emails are found.
        """
        statement: Select = self._statements.get_emails(
            entity_uuid=entity_uuid, limit=limit, offset=offset
        )
        emails: List[EmailsRes] = await self._db_ops.return_all_rows(
            service=cnst.EMAILS_READ_SERVICE, statement=statement, db=db
        )
        return record_not_exist(instance=emails, exception=EmailNotExist)

    async def get_email_ct(
        self,
        entity_uuid: UUID4,
        db: AsyncSession,
    ) -> int:
        """
        Retrieves the total count of emails associated with a given entity UUID.

        :param entity_uuid: The UUID of the entity to count the emails for.
        :type entity_uuid: UUID4
        :param db: The database session.
        :type db: AsyncSession
        :return: The total count of emails.
        :rtype: int
        """
        statement: Select = self._statements.get_email_ct(entity_uuid=entity_uuid)
        return await self._db_ops.return_count(
            service=cnst.EMAILS_READ_SERVICE, statement=statement, db=db
        )

    async def paginated_emails(
        self, entity_uuid: UUID4, page: int, limit: int, db: AsyncSession
    ) -> EmailsPgRes:
        """
        Retrieves a paginated list of emails along with pagination metadata (total count, current page, etc.).

        :param entity_uuid: The UUID of the entity to which the emails belong.
        :type entity_uuid: UUID4
        :param page: The page number for pagination.
        :type page: int
        :param limit: The maximum number of emails per page.
        :type limit: int
        :param db: The database session.
        :type db: AsyncSession
        :return: A paginated result including emails and pagination metadata.
        :rtype: EmailsPgRes
        """
        total_count: int = await self.get_email_ct(entity_uuid=entity_uuid, db=db)
        offset: int = pagination.page_offset(page=page, limit=limit)
        has_more: bool = pagination.has_more_items(
            total_count=total_count, page=page, limit=limit
        )
        emails: List[EmailsRes] = await self.get_emails(
            entity_uuid=entity_uuid, offset=offset, limit=limit, db=db
        )
        return EmailsPgRes(
            total=total_count, page=page, limit=limit, has_more=has_more, emails=emails
        )


class CreateSrvc:
    """
    Service for creating emails in the database.

    This class provides functionality to create a new email in the database.

    :param statements: The SQL statements used for creating email data.
    :type statements: EmailsStms
    :param db_operations: The database operations object used for executing queries.
    :type db_operations: Operations
    :param model: The email model used for creating email records.
    :type model: Emails
    """

    def __init__(
        self, statements: EmailsStms, db_operations: Operations, model: Emails
    ) -> None:
        """
        Initializes the CreateSrvc class with the provided statements, database operations, and model.

        :param statements: The SQL statements used for creating email data.
        :type statements: EmailsStms
        :param db_operations: The database operations object used for executing queries.
        :type db_operations: Operations
        :param model: The email model used for creating email records.
        :type model: Emails
        """
        self._statements: EmailsStms = statements
        self._db_ops: Operations = db_operations
        self._model: Emails = model

    @property
    def statements(self) -> EmailsStms:
        """
        Returns the email-related SQL statements.

        :return: The email-related SQL statements.
        :rtype: EmailsStms
        """
        return self._statements

    @property
    def db_operations(self) -> Operations:
        """
        Returns the database operations object.

        :return: The database operations object.
        :rtype: Operations
        """
        return self._db_ops

    @property
    def model(self) -> Emails:
        """
        Returns the email model.

        :return: The email model.
        :rtype: Emails
        """
        return self._model

    async def create_email(
        self,
        entity_uuid: UUID4,
        email_data: EmailsCreate,
        db: AsyncSession,
    ):
        """
        Creates a new email in the database.

        :param entity_uuid: The UUID of the entity to associate with the email.
        :type entity_uuid: UUID4
        :param email_data: The data required to create the email.
        :type email_data: EmailsCreate
        :param db: The database session.
        :type db: AsyncSession
        :return: The result of the email creation operation.
        :rtype: EmailsRes
        :raises EmailExists: If an email already exists for the given entity.
        :raises EmailNotExist: If the email could not be created.
        """
        emails = self._model
        statement = self._statements.get_email_by_email(
            entity_uuid=entity_uuid, email=email_data.email
        )
        email_exists: EmailsRes = await self._db_ops.return_one_row(
            service=cnst.EMAILS_CREATE_SERVICE, statement=statement, db=db
        )
        record_exists(instance=email_exists, exception=EmailExists)

        email = await self._db_ops.add_instance(
            service=cnst.EMAILS_CREATE_SERVICE, model=emails, data=email_data, db=db
        )
        return record_not_exist(instance=email, exception=EmailNotExist)


class UpdateSrvc:
    """
    Service for updating emails in the database.

    This class provides functionality to update email records in the database.

    :param statements: The SQL statements used for updating email data.
    :type statements: EmailsStms
    :param db_operations: The database operations object used for executing queries.
    :type db_operations: Operations
    """

    def __init__(self, statements: EmailsStms, db_operations: Operations) -> None:
        """
        Initializes the UpdateSrvc class with the provided statements and database operations.

        :param statements: The SQL statements used for updating email data.
        :type statements: EmailsStms
        :param db_operations: The database operations object used for executing queries.
        :type db_operations: Operations
        """
        self._statements: EmailsStms = statements
        self._db_ops: Operations = db_operations

    @property
    def statements(self) -> EmailsStms:
        """
        Returns the email-related SQL statements.

        :return: The email-related SQL statements.
        :rtype: EmailsStms
        """
        return self._statements

    @property
    def db_operations(self) -> Operations:
        """
        Returns the database operations object.

        :return: The database operations object.
        :rtype: Operations
        """
        return self._db_ops

    async def update_email(
        self,
        entity_uuid: UUID4,
        email_uuid: UUID4,
        email_data: EmailsUpdate,
        db: AsyncSession,
    ) -> EmailsRes:
        """
        Updates an email in the database.

        :param entity_uuid: The UUID of the entity to which the email belongs.
        :type entity_uuid: UUID4
        :param email_uuid: The UUID of the email to update.
        :type email_uuid: UUID4
        :param email_data: The data to update the email with.
        :type email_data: EmailsUpdate
        :param db: The database session.
        :type db: AsyncSession
        :return: The updated email data.
        :rtype: EmailsRes
        :raises EmailNotExist: If the email does not exist.
        """
        statement: update = self._db_ops.update_email(
            entity_uuid=entity_uuid, email_uuid=email_uuid, email_data=email_data
        )
        email: EmailsRes = await Operations.return_one_row(
            service=cnst.EMAILS_UPDATE_SERVICE, statement=statement, db=db
        )
        return record_not_exist(instance=email, exception=EmailNotExist)


class DelSrvc:
    """
    Service for deleting emails in the database.

    This class provides functionality to perform soft deletion of emails in the database.

    :param statements: The SQL statements used for deleting email data.
    :type statements: EmailsStms
    :param db_operations: The database operations object used for executing queries.
    :type db_operations: Operations
    """

    def __init__(self, statements: EmailsStms, db_operations: Operations) -> None:
        """
        Initializes the DelSrvc class with the provided statements and database operations.

        :param statements: The SQL statements used for deleting email data.
        :type statements: EmailsStms
        :param db_operations: The database operations object used for executing queries.
        :type db_operations: Operations
        """
        self._statements: EmailsStms = statements
        self._db_ops: Operations = db_operations

    @property
    def statements(self) -> EmailsStms:
        """
        Returns the email-related SQL statements.

        :return: The email-related SQL statements.
        :rtype: EmailsStms
        """
        return self._statements

    @property
    def db_operations(self) -> Operations:
        """
        Returns the database operations object.

        :return: The database operations object.
        :rtype: Operations
        """
        return self._db_ops

    async def soft_del_email(
        self,
        entity_uuid: UUID4,
        email_uuid: UUID4,
        email_data: EmailsDel,
        db: AsyncSession,
    ) -> EmailsDelRes:
        """
        Soft deletes an email in the database.

        :param entity_uuid: The UUID of the entity to which the email belongs.
        :type entity_uuid: UUID4
        :param email_uuid: The UUID of the email to delete.
        :type email_uuid: UUID4
        :param email_data: The data for performing the soft delete of the email.
        :type email_data: EmailsDel
        :param db: The database session.
        :type db: AsyncSession
        :return: The result of the soft delete operation.
        :rtype: EmailsDelRes
        :raises EmailNotExist: If the email does not exist.
        """
        statement: update = self._statements.update_email(
            entity_uuid=entity_uuid, email_uuid=email_uuid, email_data=email_data
        )
        email: EmailsDelRes = await self._db_ops.return_one_row(
            service=cnst.EMAILS_DEL_SERVICE, statement=statement, db=db
        )
        return record_not_exist(instance=email, exception=EmailNotExist)
