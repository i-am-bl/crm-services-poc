from typing import Tuple

from fastapi import APIRouter, Depends, Response, status
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from ...database.database import get_db, transaction_manager
from ...exceptions import WebsitesExists, WebsitesNotExist
from ...handlers.handler import handle_exceptions
from ...schemas import websites as s_websites
from ...services.authetication import SessionService, TokenService
from ...services.websites import WebsitesServices
from ...utilities.set_values import SetSys
from ...utilities.utilities import Pagination as pg

serv_web_c = WebsitesServices.CreateService()
serv_web_r = WebsitesServices.ReadService()
serv_web_u = WebsitesServices.UpdateService()
serv_web_d = WebsitesServices.DelService()
serv_session = SessionService()
serv_token = TokenService()
router = APIRouter()


@router.get(
    "/{entity_uuid}/websites/{website_uuid}/",
    response_model=s_websites.WebsitesResponse,
    status_code=status.HTTP_200_OK,
    include_in_schema=False,
)
@serv_token.set_auth_cookie
@handle_exceptions([WebsitesNotExist])
async def get_website(
    response: Response,
    entity_uuid: UUID4,
    website_uuid: UUID4,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple = Depends(serv_session.validate_session),
) -> s_websites.WebsitesResponse:
    """Retrieve single website by entity_uuid and website_uuid"""

    async with transaction_manager(db=db):
        return await serv_web_r.get_website(
            entity_uuid=entity_uuid,
            website_uuid=website_uuid,
            db=db,
        )


@router.get(
    "/{entity_uuid}/websites/",
    response_model=s_websites.WebsitesPagResponse,
    status_code=status.HTTP_200_OK,
)
@serv_token.set_auth_cookie
@handle_exceptions([WebsitesNotExist])
async def get_website(
    response: Response,
    entity_uuid: UUID4,
    page: int,
    limit: int,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple = Depends(serv_session.validate_session),
) -> s_websites.WebsitesPagResponse:
    """
    Get many websites by entity_uuid.
    """

    async with transaction_manager(db=db):
        offset = pg.pagination_offset(page=page, limit=limit)
        total_count = await serv_web_r.get_websites_ct(entity_uuid=entity_uuid)
        websites = await serv_web_r.get_websites(
            entity_uuid=entity_uuid, offset=offset, limit=limit, db=db
        )
        has_moore = pg.has_more(total_count=total_count, page=page, limit=limit)
        return s_websites.WebsitesPagResponse(
            total=total_count,
            page=page,
            limit=limit,
            has_more=has_moore,
            websites=websites,
        )


@router.post(
    "/{entity_uuid}/websites/",
    response_model=s_websites.WebsitesResponse,
    status_code=status.HTTP_201_CREATED,
)
@serv_token.set_auth_cookie
@handle_exceptions([WebsitesNotExist, WebsitesExists])
async def create_website(
    response: Response,
    website_data: s_websites.WebsitesCreate,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple = Depends(serv_session.validate_session),
) -> s_websites.WebsitesResponse:
    """
    Create a single entity website record.
    """

    async with transaction_manager(db=db):
        sys_user, _ = user_token
        SetSys.sys_created_by(data=website_data, sys_user=sys_user)
        return await serv_web_c.create_website(website_data=website_data, db=db)


@router.put(
    "/{entity_uuid}/websites/{website_uuid}/",
    response_model=s_websites.WebsitesResponse,
    status_code=status.HTTP_200_OK,
)
@serv_token.set_auth_cookie
@handle_exceptions([WebsitesNotExist])
async def update_website(
    response: Response,
    entity_uuid: UUID4,
    website_uuid: UUID4,
    website_data: s_websites.WebsitesUpdate,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple = Depends(serv_session.validate_session),
) -> s_websites.WebsitesResponse:
    """
    Update one website.
    """

    async with transaction_manager(db=db):
        sys_user, _ = user_token
        SetSys.sys_updated_by(data=website_data, sys_user=sys_user)
        return await serv_web_u.update_website(
            entity_uuid=entity_uuid,
            website_uuid=website_uuid,
            website_data=website_data,
            db=db,
        )


@router.delete(
    "/{entity_uuid}/websites/{website_uuid}/",
    response_model=s_websites.WebsiteDelReponse,
    status_code=status.HTTP_200_OK,
)
@serv_token.set_auth_cookie
@handle_exceptions([WebsitesNotExist])
async def soft_del_website(
    response: Response,
    entity_uuid: UUID4,
    website_uuid: UUID4,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple = Depends(serv_session.validate_session),
) -> s_websites.WebsiteDelReponse:
    """
    Soft del one website.
    """

    async with transaction_manager(db=db):
        website_data = s_websites.WebsitesSoftDel()
        sys_user, _ = user_token
        SetSys.sys_deleted_by(data=website_data, sys_user=sys_user)
        return await serv_web_d.soft_del_website(
            entity_uuid=entity_uuid,
            website_uuid=website_uuid,
            website_data=website_data,
            db=db,
        )
