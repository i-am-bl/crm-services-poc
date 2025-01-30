from pydantic import UUID4
from sqlalchemy import Select, and_, func, update

from ..models.emails import Emails
from ..utilities.data import set_empty_strs_null


class EmailsStms:
    def __init__(self, model: Emails) -> None:
        self._emails = model

    def get_email_by_email(self, entity_uuid: UUID4, email: str) -> Select:
        emails = self._emails
        return Select(emails).where(
            and_(
                emails.entity_uuid == entity_uuid,
                emails.email == email,
                emails.sys_deleted_at == None,
            )
        )

    def get_emails(self, entity_uuid: UUID4, limit: int, offset: int) -> Select:
        emails = self._emails
        return (
            Select(emails)
            .where(
                and_(emails.entity_uuid == entity_uuid, emails.sys_deleted_at == None)
            )
            .offset(offset=offset)
            .limit(limit=limit)
        )

    def get_email_ct(self, entity_uuid: UUID4) -> int:
        emails = self._emails
        return (
            Select(func.count())
            .select_from(emails)
            .where(
                and_(emails.entity_uuid == entity_uuid, emails.sys_deleted_at == None)
            )
        )

    def get_email(self, entity_uuid: UUID4, email_uuid: UUID4) -> Select:
        emails = self._emails
        return Select(emails).where(
            and_(
                emails.uuid == email_uuid,
                emails.entity_uuid == entity_uuid,
                emails.sys_deleted_at == None,
            )
        )

    def update_email(
        self,
        entity_uuid: UUID4,
        email_uuid: UUID4,
        email_data: object,
    ) -> update:

        emails = self._emails
        return (
            update(emails)
            .where(
                and_(
                    emails.entity_uuid == entity_uuid,
                    emails.uuid == email_uuid,
                    emails.sys_deleted_at == None,
                )
            )
            .values(set_empty_strs_null(email_data))
            .returning(emails)
        )
