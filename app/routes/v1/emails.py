from fastapi import APIRouter, Depends, status, Query


from pydantic import UUID4

from sqlalchemy.ext.asyncio import AsyncSession


import app.schemas.emails as s_emails
from app.database.database import get_db
from app.logger import logger
from app.services.emails import EmailsServices
from app.service_utils import pagination_offset

router = APIRouter()

serv_email_c = EmailsServices.CreateService()
serv_email_r = EmailsServices.ReadService()
serv_email_u = EmailsServices.UpdateService()
serv_email_d = EmailsServices.DelService()


@router.get(
    "/v1/entity-management/entities/{entity_uuid}/emails/{email_uuid}",
    response_model=s_emails.EmailsRespone,
    status_code=status.HTTP_200_OK,
)
async def get_email(
    entity_uuid: UUID4, email_uuid: UUID4, db: AsyncSession = Depends(get_db)
):
    """get one entity email"""
    async with db.begin():
        email = await serv_email_r.get_email(
            entity_uuid=entity_uuid, email_uuid=email_uuid, db=db
        )
        return email


@router.get(
    "/v1/entity-management/entities/{entity_uuid}/emails/",
    response_model=s_emails.EmailsPagRespone,
    status_code=status.HTTP_200_OK,
)
async def get_emails(
    entity_uuid: UUID4,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """get many emails by entity"""

    async with db.begin():
        offset = pagination_offset(page=page, limit=limit)
        total_count = await serv_email_r.get_email_ct(entity_uuid=entity_uuid, db=db)
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


@router.post(
    "/v1/entity-management/entities/{entity_uuid}/emails/",
    response_model=s_emails.EmailsRespone,
    status_code=status.HTTP_201_CREATED,
)
async def create_email(
    entity_uuid, email_data: s_emails.EmailsCreate, db: AsyncSession = Depends(get_db)
):
    async with db.begin():
        email = await serv_email_c.create_email(
            entity_uuid=entity_uuid, email_data=email_data, db=db
        )
    return email


@router.put(
    "/v1/entity-management/entities/{entity_uuid}/emails/{email_uuid}",
    response_model=s_emails.EmailsRespone,
    status_code=status.HTTP_200_OK,
)
async def update_email(
    entity_uuid: UUID4,
    email_uuid: UUID4,
    email_data: s_emails.EmailsUpdate,
    db: AsyncSession = Depends(get_db),
):
    """update one email"""
    async with db.begin():
        email = await serv_email_u.update_email(
            entity_uuid=entity_uuid, email_uuid=email_uuid, email_data=email_data, db=db
        )
        return email


@router.delete(
    "/v1/entity-management/entities/{entity_uuid}/emails/{email_uuid}",
    response_model=s_emails.EmailsDelResponse,
    status_code=status.HTTP_200_OK,
)
async def soft_del_email(
    entity_uuid: UUID4,
    email_uuid: UUID4,
    email_data: s_emails.EmailsDel,
    db: AsyncSession = Depends(get_db),
):
    """soft del one email"""
    async with db.begin():
        email = await serv_email_d.soft_del_email(
            entity_uuid=entity_uuid, email_uuid=email_uuid, email_data=email_data, db=db
        )
        return email
