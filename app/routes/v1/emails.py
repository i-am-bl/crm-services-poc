from fastapi import APIRouter, Depends, Query, Request, Response, status
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

import app.schemas.emails as s_emails

from ...database.database import get_db
from ...services.authetication import SessionService
from ...services.emails import EmailsServices
from ...utilities.logger import logger
from ...utilities.service_utils import pagination_offset
from ...utilities.sys_users import SetSys
from ...exceptions import UnhandledException, EmailNotExist, EmailExists

router = APIRouter()

serv_email_c = EmailsServices.CreateService()
serv_email_r = EmailsServices.ReadService()
serv_email_u = EmailsServices.UpdateService()
serv_email_d = EmailsServices.DelService()
serv_session = SessionService()


@router.get(
    "/v1/entity-management/entities/{entity_uuid}/emails/{email_uuid}",
    response_model=s_emails.EmailsRespone,
    status_code=status.HTTP_200_OK,
)
async def get_email(
    request: Request,
    response: Response,
    entity_uuid: UUID4,
    email_uuid: UUID4,
    db: AsyncSession = Depends(get_db),
):
    """get one entity email"""
    try:
        async with db.begin():
            _ = await serv_session.validate_session(
                request=request, response=response, db=db
            )
            email = await serv_email_r.get_email(
                entity_uuid=entity_uuid, email_uuid=email_uuid, db=db
            )
            return email
    except EmailNotExist:
        raise EmailNotExist()
    except Exception:
        raise UnhandledException()


@router.get(
    "/v1/entity-management/entities/{entity_uuid}/emails/",
    response_model=s_emails.EmailsPagRespone,
    status_code=status.HTTP_200_OK,
)
async def get_emails(
    request: Request,
    response: Response,
    entity_uuid: UUID4,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """get many emails by entity"""

    try:
        async with db.begin():
            _ = await serv_session.validate_session(
                request=request, response=response, db=db
            )
            offset = pagination_offset(page=page, limit=limit)
            total_count = await serv_email_r.get_email_ct(
                entity_uuid=entity_uuid, db=db
            )
            emails = await serv_email_r.get_emails(
                entity_uuid=entity_uuid, limit=limit, offset=offset, db=db
            )

            return {
                "total": total_count,
                "page": page,
                "limit": limit,
                "has_more": total_count > (page * limit),
                "emails": emails,
            }
    except EmailNotExist:
        raise EmailNotExist()
    except Exception:
        raise UnhandledException()


@router.post(
    "/v1/entity-management/entities/{entity_uuid}/emails/",
    response_model=s_emails.EmailsRespone,
    status_code=status.HTTP_201_CREATED,
)
async def create_email(
    request: Request,
    response: Response,
    entity_uuid,
    email_data: s_emails.EmailsCreate,
    db: AsyncSession = Depends(get_db),
):
    try:
        async with db.begin():
            sys_user = await serv_session.validate_session(
                request=request, response=response, db=db
            )
            SetSys.sys_created_by(data=email_data, sys_user=sys_user)
            email = await serv_email_c.create_email(
                entity_uuid=entity_uuid, email_data=email_data, db=db
            )
        return email
    except EmailNotExist:
        raise EmailNotExist()
    except EmailExists:
        raise EmailExists()
    except Exception:
        raise UnhandledException()


@router.put(
    "/v1/entity-management/entities/{entity_uuid}/emails/{email_uuid}",
    response_model=s_emails.EmailsRespone,
    status_code=status.HTTP_200_OK,
)
async def update_email(
    request: Request,
    response: Response,
    entity_uuid: UUID4,
    email_uuid: UUID4,
    email_data: s_emails.EmailsUpdate,
    db: AsyncSession = Depends(get_db),
):
    """update one email"""
    try:
        async with db.begin():
            sys_user = await serv_session.validate_session(
                request=request, response=response, db=db
            )
            SetSys.sys_updated_by(data=email_data, sys_user=sys_user)
            email = await serv_email_u.update_email(
                entity_uuid=entity_uuid,
                email_uuid=email_uuid,
                email_data=email_data,
                db=db,
            )
            return email
    except EmailNotExist:
        raise EmailNotExist()
    except Exception:
        raise UnhandledException()


@router.delete(
    "/v1/entity-management/entities/{entity_uuid}/emails/{email_uuid}",
    response_model=s_emails.EmailsDelResponse,
    status_code=status.HTTP_200_OK,
)
async def soft_del_email(
    request: Request,
    response: Response,
    entity_uuid: UUID4,
    email_uuid: UUID4,
    email_data: s_emails.EmailsDel,
    db: AsyncSession = Depends(get_db),
):
    """soft del one email"""
    try:
        async with db.begin():
            sys_user = await serv_session.validate_session(
                request=request, response=response, db=db
            )
            SetSys.sys_deleted_by(data=email_data, sys_user=sys_user)
            email = await serv_email_d.soft_del_email(
                entity_uuid=entity_uuid,
                email_uuid=email_uuid,
                email_data=email_data,
                db=db,
            )
            return email
    except EmailNotExist:
        raise EmailNotExist()
    except Exception:
        raise UnhandledException()
