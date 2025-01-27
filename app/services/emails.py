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
from ..utilities.utilities import DataUtils as di


class ReadSrvc:
    def __init__(self, statements: EmailsStms, db_operations) -> None:
        self._statements: EmailsStms = statements
        self._db_ops: Operations = db_operations

    @property
    def statements(self) -> EmailsStms:
        return self._statements

    @property
    def db_operations(self) -> Operations:
        return self._db_ops

    async def get_email(
        self,
        entity_uuid: UUID4,
        email_uuid: UUID4,
        db: AsyncSession,
    ) -> EmailsRes:
        statement: Select = self._statements.get_email(
            entity_uuid=entity_uuid, email_uuid=email_uuid
        )
        email: EmailsRes = await self._db_ops.return_one_row(
            service=cnst.EMAILS_READ_SERVICE, statement=statement, db=db
        )
        return di.record_not_exist(instance=email, exception=EmailNotExist)

    async def get_emails(
        self,
        entity_uuid: UUID4,
        limit: int,
        offset: int,
        db: AsyncSession,
    ) -> List[EmailsRes]:
        statement: Select = self._statements.get_emails(
            entity_uuid=entity_uuid, limit=limit, offset=offset
        )
        emails: List[EmailsRes] = await self._db_ops.return_all_rows(
            service=cnst.EMAILS_READ_SERVICE, statement=statement, db=db
        )
        return di.record_not_exist(instance=emails, exception=EmailNotExist)

    async def get_email_ct(
        self,
        entity_uuid: UUID4,
        db: AsyncSession,
    ) -> int:
        statement: Select = self._statements.get_email_ct(entity_uuid=entity_uuid)
        return await self._db_ops.return_count(
            service=cnst.EMAILS_READ_SERVICE, statement=statement, db=db
        )

    async def paginated_emails(
        self, entity_uuid: UUID4, page: int, limit: int, db: AsyncSession
    ) -> EmailsPgRes:

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
    def __init__(
        self, statements: EmailsStms, db_operations: Operations, model: Emails
    ) -> None:
        self._statements: EmailsStms = statements
        self._db_ops: Operations = db_operations
        self._model: Emails = model

    @property
    def statements(self) -> EmailsStms:
        return self._statements

    @property
    def db_operations(self) -> Operations:
        return self._db_ops

    @property
    def model(self) -> Emails:
        return self._model

    async def create_email(
        self,
        entity_uuid: UUID4,
        email_data: EmailsCreate,
        db: AsyncSession,
    ):
        emails = self._model
        statement = self._statements.get_email_by_email(
            entity_uuid=entity_uuid, email=email_data.email
        )
        email_exists: EmailsRes = await self._db_ops.return_one_row(
            service=cnst.EMAILS_CREATE_SERVICE, statement=statement, db=db
        )
        di.record_exists(instance=email_exists, exception=EmailExists)

        email = await self._db_ops.add_instance(
            service=cnst.EMAILS_CREATE_SERVICE, model=emails, data=email_data, db=db
        )
        return di.record_not_exist(instance=email, exception=EmailNotExist)


class UpdateSrvc:
    def __init__(self, statements: EmailsStms, db_operations: Operations) -> None:
        self._statements: EmailsStms = statements
        self._db_ops: Operations = db_operations

    @property
    def statements(self) -> EmailsStms:
        return self._statements

    @property
    def db_operations(self) -> Operations:
        return self._db_ops

    async def update_email(
        self,
        entity_uuid: UUID4,
        email_uuid: UUID4,
        email_data: EmailsUpdate,
        db: AsyncSession,
    ) -> EmailsRes:
        statment: update = self._db_ops.update_email(
            entity_uuid=entity_uuid, email_uuid=email_uuid, email_data=email_data
        )
        email: EmailsRes = await Operations.return_one_row(
            service=cnst.EMAILS_UPDATE_SERVICE, statement=statment, db=db
        )
        return di.record_not_exist(instance=email, exception=EmailNotExist)


class DelSrvc:
    def __init__(self, statements: EmailsStms, db_operations: Operations) -> None:
        self._statements: EmailsStms = statements
        self._db_ops: Operations = db_operations

    @property
    def statements(self) -> EmailsStms:
        return self._statements

    @property
    def db_operations(self) -> Operations:
        return self._db_ops

    async def soft_del_email(
        self,
        entity_uuid: UUID4,
        email_uuid: UUID4,
        email_data: EmailsDel,
        db: AsyncSession,
    ) -> EmailsDelRes:
        statement: update = self._statements.update_email(
            entity_uuid=entity_uuid, email_uuid=email_uuid, email_data=email_data
        )
        email: EmailsDelRes = await self._db_ops.return_one_row(
            service=cnst.EMAILS_DEL_SERVICE, statement=statement, db=db
        )
        return di.record_not_exist(instance=email, exception=EmailNotExist)
