from math import e
from fastapi import Depends
from pydantic import UUID4
from sqlalchemy import Select, update, and_, func
from sqlalchemy.ext.asyncio import AsyncSession

import app.constants as cnst
import app.models.emails as m_emails
import app.schemas.emails as s_emails
from app.database.database import Operations, get_db
from app.logger import logger
from app.schemas._variables import ConstrainedEmailStr
from app.services.utilities import DataUtils as di


class EmailModels:
    emails = m_emails.Emails


class EmailStatements:
    pass

    class SelStatements:
        pass

        @staticmethod
        def sel_email_by_entity_email(entity_uuid: UUID4, email: ConstrainedEmailStr):

            emails = EmailModels.emails
            statement = Select(emails).where(
                and_(
                    emails.entity_uuid == entity_uuid,
                    emails.email == email,
                )
            )
            return statement

        @staticmethod
        def sel_email_by_entity(entity_uuid: UUID4, limit: int, offset: int):
            emails = EmailModels.emails
            statement = (
                Select(emails)
                .where(
                    and_(
                        emails.entity_uuid == entity_uuid, emails.sys_deleted_at == None
                    )
                )
                .offset(offset=offset)
                .limit(limit=limit)
            )
            return statement

        @staticmethod
        def sel_email_by_entity_ct(entity_uuid: UUID4):
            emails = EmailModels.emails
            statement = (
                Select(func.count())
                .select_from(emails)
                .where(
                    and_(
                        emails.entity_uuid == entity_uuid, emails.sys_deleted_at == None
                    )
                )
            )
            return statement

        @staticmethod
        def sel_email_by_entity_email_uuid(entity_uuid: UUID4, email_uuid: UUID4):

            emails = EmailModels.emails
            statement = Select(emails).where(
                and_(
                    emails.uuid == email_uuid,
                    emails.entity_uuid == entity_uuid,
                )
            )
            return statement

    class UpdateStatements:
        pass

        @staticmethod
        def update_email_stm(
            entity_uuid: UUID4,
            email_uuid: UUID4,
            email_data: object,
        ):

            emails = EmailModels.emails
            statement = (
                update(emails)
                .where(
                    and_(
                        emails.entity_uuid == entity_uuid,
                        emails.uuid == email_uuid,
                    )
                )
                .values(di.set_empty_strs_null(email_data))
                .returning(emails)
            )

            return statement


class EmailsServices:
    pass

    class ReadService:
        def __init__(self) -> None:
            pass

        async def get_email(
            self,
            entity_uuid: UUID4,
            email_uuid: UUID4,
            db: AsyncSession = Depends(get_db),
        ):
            statement = EmailStatements.SelStatements.sel_email_by_entity_email_uuid(
                entity_uuid=entity_uuid, email_uuid=email_uuid
            )
            email = await Operations.return_one_row(
                service=cnst.EMAILS_READ_SERVICE, statement=statement, db=db
            )
            # di.rec_not_exist_or_soft_del(email)
            return email

        async def get_emails(
            self,
            entity_uuid: UUID4,
            limit: int,
            offset: int,
            db: AsyncSession = Depends(get_db),
        ):
            statement = EmailStatements.SelStatements.sel_email_by_entity(
                entity_uuid=entity_uuid, limit=limit, offset=offset
            )
            emails = await Operations.return_all_rows(
                service=cnst.EMAILS_READ_SERVICE, statement=statement, db=db
            )

            return emails

        async def get_email_ct(
            self,
            entity_uuid: UUID4,
            db: AsyncSession = Depends(get_db),
        ):
            statement = EmailStatements.SelStatements.sel_email_by_entity_ct(
                entity_uuid=entity_uuid
            )
            emails = await Operations.return_count(
                service=cnst.EMAILS_READ_SERVICE, statement=statement, db=db
            )
            return emails

    class CreateService:
        def __init__(self) -> None:
            pass

        async def create_email(
            self,
            entity_uuid: UUID4,
            email_data: s_emails.EmailsCreate,
            db: AsyncSession = Depends(get_db),
        ):
            emails = EmailModels.emails
            statement = EmailStatements.SelStatements.sel_email_by_entity_email(
                entity_uuid=entity_uuid, email=email_data.email
            )
            email_exists = await Operations.return_one_row(
                service=cnst.EMAILS_CREATE_SERVICE, statement=statement, db=db
            )
            di.record_exists(email_exists)

            email = await Operations.add_instance(
                service=cnst.EMAILS_CREATE_SERVICE, model=emails, data=email_data, db=db
            )
            return email

    class UpdateService:
        def __init__(self) -> None:
            pass

        async def update_email(
            self,
            entity_uuid: UUID4,
            email_uuid: UUID4,
            email_data: s_emails.EmailsUpdate,
            db: AsyncSession = Depends(get_db),
        ):
            statment = EmailStatements.UpdateStatements.update_email_stm(
                entity_uuid=entity_uuid, email_uuid=email_uuid, email_data=email_data
            )
            email = await Operations.return_one_row(
                service=cnst.EMAILS_UPDATE_SERVICE, statement=statment, db=db
            )
            di.rec_not_exist_or_soft_del(email)
            return email

    class DelService:
        def __init__(self) -> None:
            pass

        async def soft_del_email(
            self,
            entity_uuid: UUID4,
            email_uuid: UUID4,
            email_data: s_emails.EmailsDel,
            db: AsyncSession = Depends(get_db),
        ):
            statement = EmailStatements.UpdateStatements.update_email_stm(
                entity_uuid=entity_uuid, email_uuid=email_uuid, email_data=email_data
            )
            email = await Operations.return_one_row(
                service=cnst.EMAILS_DEL_SERVICE, statement=statement, db=db
            )
            di.record_not_exist(email)
            return email