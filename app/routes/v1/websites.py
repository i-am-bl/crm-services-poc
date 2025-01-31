from typing import Tuple

from fastapi import APIRouter, Depends, Response, status
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from ...containers.services import container as service_container
from ...database.database import get_db, transaction_manager
from ...exceptions import WebsitesExists, WebsitesNotExist
from ...handlers.handler import handle_exceptions
from ...models.sys_users import SysUsers
from ...schemas.websites import (
    WebsitesCreate,
    WebsitesInternalCreate,
    WebsitesInternalUpdate,
    WebsitesPgRes,
    WebsitesDel,
    WebsitesUpdate,
    WebsitesRes,
)
from ...services.websites import CreateSrvc, ReadSrvc, UpdateSrvc, DelSrvc
from ...services.token import set_auth_cookie
from ...utilities import sys_values
from ...utilities.auth import get_validated_session
from ...utilities.data import internal_schema_validation

router = APIRouter()


@router.get(
    "/{entity_uuid}/websites/{website_uuid}/",
    response_model=WebsitesRes,
    status_code=status.HTTP_200_OK,
    include_in_schema=False,
)
@set_auth_cookie
@handle_exceptions([WebsitesNotExist])
async def get_website(
    response: Response,
    entity_uuid: UUID4,
    website_uuid: UUID4,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple[SysUsers, str] = Depends(get_validated_session),
    websites_read_srvc: ReadSrvc = Depends(service_container["websites_read"]),
) -> WebsitesRes:
    """Retrieve single website by entity_uuid and website_uuid"""

    async with transaction_manager(db=db):
        return await websites_read_srvc.get_website(
            entity_uuid=entity_uuid,
            website_uuid=website_uuid,
            db=db,
        )


@router.get(
    "/{entity_uuid}/websites/",
    response_model=WebsitesPgRes,
    status_code=status.HTTP_200_OK,
)
@set_auth_cookie
@handle_exceptions([WebsitesNotExist])
async def get_website(
    response: Response,
    entity_uuid: UUID4,
    page: int,
    limit: int,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple[SysUsers, str] = Depends(get_validated_session),
    websites_read_srvc: ReadSrvc = Depends(service_container["websites_read"]),
) -> WebsitesPgRes:
    """
    Get many websites by entity_uuid.
    """

    async with transaction_manager(db=db):
        return await websites_read_srvc.paginated_websites(
            entity_uuid=entity_uuid, page=page, limit=limit, db=db
        )


@router.post(
    "/{entity_uuid}/websites/",
    response_model=WebsitesRes,
    status_code=status.HTTP_201_CREATED,
)
@set_auth_cookie
@handle_exceptions([WebsitesNotExist, WebsitesExists])
async def create_website(
    response: Response,
    website_data: WebsitesCreate,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple[SysUsers, str] = Depends(get_validated_session),
    websites_create_srvc: CreateSrvc = Depends(service_container["websites_create"]),
) -> WebsitesRes:
    """
    Create a single entity website record.
    """

    sys_user, _ = user_token
    _website_data: WebsitesInternalCreate = internal_schema_validation(
        data=website_data,
        schema=WebsitesInternalCreate,
        setter_method=sys_values.sys_created_by,
        sys_user_uuid=sys_user.uuid,
    )

    async with transaction_manager(db=db):
        return await websites_create_srvc.create_website(
            website_data=_website_data, db=db
        )


@router.put(
    "/{entity_uuid}/websites/{website_uuid}/",
    response_model=WebsitesRes,
    status_code=status.HTTP_200_OK,
)
@set_auth_cookie
@handle_exceptions([WebsitesNotExist])
async def update_website(
    response: Response,
    entity_uuid: UUID4,
    website_uuid: UUID4,
    website_data: WebsitesUpdate,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple[SysUsers, str] = Depends(get_validated_session),
    websites_update_srvc: UpdateSrvc = Depends(service_container["websites_update"]),
) -> WebsitesRes:
    """
    Update one website.
    """

    sys_user, _ = user_token
    _website_data: WebsitesInternalUpdate = internal_schema_validation(
        data=website_data,
        schema=WebsitesInternalUpdate,
        setter_method=sys_values.sys_updated_by,
        sys_user_uuid=sys_user.uuid,
    )

    async with transaction_manager(db=db):
        return await websites_update_srvc.update_website(
            entity_uuid=entity_uuid,
            website_uuid=website_uuid,
            website_data=_website_data,
            db=db,
        )


@router.delete(
    "/{entity_uuid}/websites/{website_uuid}/",
    status_code=status.HTTP_204_NO_CONTENT,
)
@set_auth_cookie
@handle_exceptions([WebsitesNotExist])
async def soft_del_website(
    response: Response,
    entity_uuid: UUID4,
    website_uuid: UUID4,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple[SysUsers, str] = Depends(get_validated_session),
    websites_delete_srvc: DelSrvc = Depends(service_container["websites_delete"]),
) -> None:
    """
    Soft del one website.
    """

    sys_user, _ = user_token
    _website_data: WebsitesDel = internal_schema_validation(
        schema=WebsitesDel,
        setter_method=sys_values.sys_deleted_by,
        sys_user_uuid=sys_user.uuid,
    )

    async with transaction_manager(db=db):
        await websites_delete_srvc.soft_del_website(
            entity_uuid=entity_uuid,
            website_uuid=website_uuid,
            website_data=_website_data,
            db=db,
        )
