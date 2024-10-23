from typing import Tuple

from fastapi import APIRouter, Depends, Query, Response, status
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

import app.schemas.emails as s_emails

from ...database.database import get_db, transaction_manager
from ...exceptions import EmailExists, EmailNotExist
from ...handlers.handler import handle_exceptions
from ...services.authetication import SessionService, TokenService
from ...services.emails import EmailsServices
from ...utilities.logger import logger
from ...utilities.set_values import SetSys
from ...utilities.utilities import Pagination as pg

router = APIRouter()

serv_email_c = EmailsServices.CreateService()
serv_email_r = EmailsServices.ReadService()
serv_email_u = EmailsServices.UpdateService()
serv_email_d = EmailsServices.DelService()
serv_session = SessionService()
serv_token = TokenService()


@router.get(
    "/{entity_uuid}/emails/{email_uuid}",
    response_model=s_emails.EmailsRespone,
    status_code=status.HTTP_200_OK,
    include_in_schema=False,
)
@serv_token.set_auth_cookie
@handle_exceptions([EmailNotExist])
async def get_email(
    response: Response,
    entity_uuid: UUID4,
    email_uuid: UUID4,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple = Depends(serv_session.validate_session),
) -> s_emails.EmailsRespone:
    """get one entity email"""

    async with transaction_manager(db=db):
        return await serv_email_r.get_email(
            entity_uuid=entity_uuid, email_uuid=email_uuid, db=db
        )


@router.get(
    "/{entity_uuid}/emails/",
    response_model=s_emails.EmailsPagRespone,
    status_code=status.HTTP_200_OK,
)
@serv_token.set_auth_cookie
@handle_exceptions([EmailNotExist])
async def get_emails(
    response: Response,
    entity_uuid: UUID4,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    user_token: Tuple = Depends(serv_session.validate_session),
) -> s_emails.EmailsPagRespone:
    """
    Get many emails by entity.
    """

    async with transaction_manager(db=db):
        offset = pg.pagination_offset(page=page, limit=limit)
        total_count = await serv_email_r.get_email_ct(entity_uuid=entity_uuid, db=db)
        emails = await serv_email_r.get_emails(
            entity_uuid=entity_uuid, limit=limit, offset=offset, db=db
        )
        has_more = pg.has_more(total_count=total_count, page=page, limit=limit)
        return s_emails.EmailsPagRespone(
            total=total_count, page=page, limit=limit, has_more=has_more, emails=emails
        )


@router.post(
    "/{entity_uuid}/emails/",
    response_model=s_emails.EmailsRespone,
    status_code=status.HTTP_201_CREATED,
)
@serv_token.set_auth_cookie
@handle_exceptions([EmailNotExist, EmailExists])
async def create_email(
    response: Response,
    entity_uuid,
    email_data: s_emails.EmailsCreate,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple = Depends(serv_session.validate_session),
) -> s_emails.EmailsCreate:
    """
    Create one email for entity.
    """

    async with transaction_manager(db=db):
        sys_user, _ = user_token
        SetSys.sys_created_by(data=email_data, sys_user=sys_user)
        return await serv_email_c.create_email(
            entity_uuid=entity_uuid, email_data=email_data, db=db
        )


@router.put(
    "/{entity_uuid}/emails/{email_uuid}",
    response_model=s_emails.EmailsRespone,
    status_code=status.HTTP_200_OK,
)
@serv_token.set_auth_cookie
@handle_exceptions([EmailNotExist])
async def update_email(
    response: Response,
    entity_uuid: UUID4,
    email_uuid: UUID4,
    email_data: s_emails.EmailsUpdate,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple = Depends(serv_session.validate_session),
) -> s_emails.EmailsUpdate:
    """
    Update one email.
    """

    async with transaction_manager(db=db):
        sys_user, _ = user_token
        SetSys.sys_updated_by(data=email_data, sys_user=sys_user)
        return await serv_email_u.update_email(
            entity_uuid=entity_uuid,
            email_uuid=email_uuid,
            email_data=email_data,
            db=db,
        )


@router.delete(
    "/{entity_uuid}/emails/{email_uuid}",
    response_model=s_emails.EmailsDelResponse,
    status_code=status.HTTP_200_OK,
)
@serv_token.set_auth_cookie
@handle_exceptions([EmailNotExist])
async def soft_del_email(
    response: Response,
    entity_uuid: UUID4,
    email_uuid: UUID4,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple = Depends(serv_session.validate_session),
) -> s_emails.EmailsDel:
    """
    Soft del one email.
    """

    async with transaction_manager(db=db):
        email_data = s_emails.EmailsDel()
        sys_user, _ = user_token
        SetSys.sys_deleted_by(data=email_data, sys_user=sys_user)
        return await serv_email_d.soft_del_email(
            entity_uuid=entity_uuid,
            email_uuid=email_uuid,
            email_data=email_data,
            db=db,
        )
