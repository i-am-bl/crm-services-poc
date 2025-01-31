from pydantic import UUID4
from sqlalchemy import Select, and_, func, update

from ..models.emails import Emails
from ..utilities.data import set_empty_strs_null


class EmailsStms:
    """
    A class responsible for constructing SQLAlchemy queries and statements for managing emails.

    ivars:
    ivar: _emails: Emails: An instance of the Emails model.
    """

    def __init__(self, model: Emails) -> None:
        """
        Initializes the EmailsStms class.

        :param model: Emails: An instance of the Emails model.
        :return None
        """
        self._emails = model

    def get_email_by_email(self, entity_uuid: UUID4, email: str) -> Select:
        """
        Selects an email by entity_uuid and email.

        :param entity_uuid: UUID4: The UUID of the entity associated with the email.
        :param email: str: The email address to search for.
        :return: Select: A Select statement for the email.
        """
        emails = self._emails
        return Select(emails).where(
            and_(
                emails.entity_uuid == entity_uuid,
                emails.email == email,
                emails.sys_deleted_at == None,
            )
        )

    def get_emails(self, entity_uuid: UUID4, limit: int, offset: int) -> Select:
        """
        Selects emails by entity_uuid with pagination support.

        :param entity_uuid: UUID4: The UUID of the entity associated with the emails.
        :param limit: int: The number of records to return.
        :param offset: int: The number of records to skip.
        :return: Select: A Select statement for the emails.
        """
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
        """
        Selects the count of emails by entity_uuid.

        :param entity_uuid: UUID4: The UUID of the entity associated with the emails.
        :return: int: The count of emails.
        """
        emails = self._emails
        return (
            Select(func.count())
            .select_from(emails)
            .where(
                and_(emails.entity_uuid == entity_uuid, emails.sys_deleted_at == None)
            )
        )

    def get_email(self, entity_uuid: UUID4, email_uuid: UUID4) -> Select:
        """
        Selects an email by entity_uuid and email_uuid.

        :param entity_uuid: UUID4: The UUID of the entity associated with the email.
        :param email_uuid: UUID4: The UUID of the email to retrieve.
        :return: Select: A Select statement for the email.
        """
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
        """
        Updates an email by entity_uuid and email_uuid.

        :param entity_uuid: UUID4: The UUID of the entity associated with the email.
        :param email_uuid: UUID4: The UUID of the email to update.
        :param email_data: object: The data to update the email with.
        :return: update: An Update statement for the email.
        """
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
