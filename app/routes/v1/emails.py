from typing import Tuple

from fastapi import APIRouter, Depends, Query, Response, status
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from ...containers.services import container as services_container
from ...database.database import get_db, transaction_manager
from ...exceptions import EmailExists, EmailNotExist
from ...handlers.handler import handle_exceptions
from ...models.sys_users import SysUsers
from ...schemas.emails import (
    EmailsCreate,
    EmailsInternalCreate,
    EmailsInternalUpdate,
    EmailsUpdate,
    EmailsRes,
    EmailsPgRes,
    EmailsDel,
)
from ...services.emails import CreateSrvc, ReadSrvc, UpdateSrvc, DelSrvc
from ...services.token import set_auth_cookie
from ...utilities import sys_values
from ...utilities.auth import get_validated_session
from ...utilities.data import internal_schema_validation

router = APIRouter()


@router.get(
    "/{entity_uuid}/emails/{email_uuid}",
    response_model=EmailsRes,
    status_code=status.HTTP_200_OK,
    include_in_schema=False,
)
@set_auth_cookie
@handle_exceptions([EmailNotExist])
async def get_email(
    response: Response,
    entity_uuid: UUID4,
    email_uuid: UUID4,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple[SysUsers, str] = Depends(get_validated_session),
    emails_read_srvc: ReadSrvc = Depends(services_container["emails_read"]),
) -> EmailsRes:
    """get one entity email"""

    async with transaction_manager(db=db):
        return await emails_read_srvc.get_email(
            entity_uuid=entity_uuid, email_uuid=email_uuid, db=db
        )


@router.get(
    "/{entity_uuid}/emails/",
    response_model=EmailsPgRes,
    status_code=status.HTTP_200_OK,
)
@set_auth_cookie
@handle_exceptions([EmailNotExist])
async def get_emails(
    response: Response,
    entity_uuid: UUID4,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    user_token: Tuple[SysUsers, str] = Depends(get_validated_session),
    emails_read_srvc: ReadSrvc = Depends(services_container["emails_read"]),
) -> EmailsPgRes:
    """
    Get many emails by entity.
    """

    async with transaction_manager(db=db):
        return emails_read_srvc.paginated_emails(
            entity_uuid=entity_uuid, page=page, limit=limit, db=db
        )


@router.post(
    "/{entity_uuid}/emails/",
    response_model=EmailsRes,
    status_code=status.HTTP_201_CREATED,
)
@set_auth_cookie
@handle_exceptions([EmailNotExist, EmailExists])
async def create_email(
    response: Response,
    entity_uuid,
    email_data: EmailsCreate,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple[SysUsers, str] = Depends(get_validated_session),
    emails_create_srvc: CreateSrvc = Depends(services_container["emails_create"]),
) -> EmailsCreate:
    """
    Create one email for entity.
    """
    sys_user, _ = user_token
    _email_data: EmailsInternalCreate = internal_schema_validation(
        data=email_data,
        schema=EmailsInternalCreate,
        setter_method=sys_values.sys_created_by,
        sys_user_uuid=sys_user.uuid,
    )

    async with transaction_manager(db=db):
        sys_values.sys_created_by(data=email_data, sys_user_uuid=sys_user.uuid)
        return await emails_create_srvc.create_email(
            entity_uuid=entity_uuid, email_data=_email_data, db=db
        )


@router.put(
    "/{entity_uuid}/emails/{email_uuid}",
    response_model=EmailsRes,
    status_code=status.HTTP_200_OK,
)
@set_auth_cookie
@handle_exceptions([EmailNotExist])
async def update_email(
    response: Response,
    entity_uuid: UUID4,
    email_uuid: UUID4,
    email_data: EmailsUpdate,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple[SysUsers, str] = Depends(get_validated_session),
    user_update_srvc: UpdateSrvc = Depends(services_container["emails_update"]),
) -> EmailsUpdate:
    """
    Update one email.
    """
    sys_user, _ = user_token
    _email_data: EmailsInternalUpdate = internal_schema_validation(
        data=email_data,
        schema=EmailsInternalUpdate,
        setter_method=sys_values.sys_updated_by,
        sys_user_uuid=sys_user.uuid,
    )

    async with transaction_manager(db=db):

        return await user_update_srvc.update_email(
            entity_uuid=entity_uuid,
            email_uuid=email_uuid,
            email_data=_email_data,
            db=db,
        )


@router.delete(
    "/{entity_uuid}/emails/{email_uuid}",
    status_code=status.HTTP_200_OK,
)
@set_auth_cookie
@handle_exceptions([EmailNotExist])
async def soft_del_email(
    response: Response,
    entity_uuid: UUID4,
    email_uuid: UUID4,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple[SysUsers, str] = Depends(get_validated_session),
    user_delete_srvc: DelSrvc = Depends(services_container["emails_delete"]),
) -> None:
    """
    Soft del one email.
    """
    sys_user, _ = user_token
    _email_data: EmailsDel = internal_schema_validation(
        schema=EmailsDel,
        setter_method=sys_values.sys_deleted_by,
        sys_user_uuid=sys_user.uuid,
    )

    async with transaction_manager(db=db):
        return await user_delete_srvc.soft_del_email(
            entity_uuid=entity_uuid,
            email_uuid=email_uuid,
            email_data=_email_data,
            db=db,
        )
