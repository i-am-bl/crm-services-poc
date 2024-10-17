from uuid import UUID

from fastapi import APIRouter, Depends, Request, Response, status
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from ...database.database import get_db
from ...schemas import websites as s_websites
from ...services.authetication import SessionService
from ...services.websites import WebsitesServices
from ...utilities.sys_users import SetSys
from ...exceptions import UnhandledException, WebsitesExists, WebsitesNotExist

serv_web_c = WebsitesServices.CreateService()
serv_web_r = WebsitesServices.ReadService()
serv_web_u = WebsitesServices.UpdateService()
serv_web_d = WebsitesServices.DelService()
serv_session = SessionService()


router = APIRouter()


@router.get(
    "/v1/entity-management/entities/{entity_uuid}/websites/{website_uuid}/",
    response_model=s_websites.WebsitesResponse,
    status_code=status.HTTP_200_OK,
)
async def get_website(
    request: Request,
    response: Response,
    entity_uuid: UUID4,
    website_uuid: UUID4,
    db: AsyncSession = Depends(get_db),
):
    """Retrieve single website by entity_uuid and website_uuid"""
    try:
        async with db.begin():
            _ = await serv_session.validate_session(
                request=request, response=response, db=db
            )
            website = await serv_web_r.get_website(
                entity_uuid=entity_uuid,
                website_uuid=website_uuid,
                db=db,
            )
        return website
    except WebsitesNotExist:
        raise WebsitesNotExist()
    except Exception:
        raise UnhandledException()


@router.get(
    "/v1/entity-management/entities/{entity_uuid}/websites/",
    response_model=s_websites.WebsitesResponse,
    status_code=status.HTTP_200_OK,
)
async def get_website(
    request: Request,
    response: Response,
    entity_uuid: UUID4,
    website_uuid: UUID4,
    db: AsyncSession = Depends(get_db),
):
    """Retrieve all websites by entity_uuid"""
    try:
        async with db.begin():
            _ = await serv_session.validate_session(
                request=request, response=response, db=db
            )
            website = await serv_web_r.get_website(
                entity_uuid=entity_uuid,
                website_uuid=website_uuid,
                db=db,
            )
        return website
    except WebsitesNotExist:
        raise WebsitesNotExist()
    except Exception:
        raise UnhandledException()


@router.post(
    "/v1/entity-management/entities/{entity_uuid}/websites/",
    response_model=s_websites.WebsitesResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_website(
    request: Request,
    response: Response,
    website_data: s_websites.WebsitesCreate,
    db: AsyncSession = Depends(get_db),
):
    """Create a single entity website record."""
    try:
        async with db.begin():
            sys_user = await serv_session.validate_session(
                request=request, response=response, db=db
            )
            SetSys.sys_created_by(data=website_data, sys_user=sys_user)
            website = await serv_web_c.create_website(website_data=website_data, db=db)
            return website
    except WebsitesExists:
        raise WebsitesExists()
    except WebsitesNotExist:
        raise WebsitesNotExist()
    except Exception:
        raise UnhandledException()


@router.put(
    "/v1/entity-management/entities/{entity_uuid}/websites/{website_uuid}/",
    response_model=s_websites.WebsitesResponse,
    status_code=status.HTTP_200_OK,
)
async def update_website(
    request: Request,
    response: Response,
    entity_uuid: UUID4,
    website_uuid: UUID4,
    website_data: s_websites.WebsitesUpdate,
    db: AsyncSession = Depends(get_db),
):
    try:
        async with db.begin():
            sys_user = await serv_session.validate_session(
                request=request, response=response, db=db
            )
            SetSys.sys_updated_by(data=website_data, sys_user=sys_user)
            website = await serv_web_u.update_website(
                entity_uuid=entity_uuid,
                website_uuid=website_uuid,
                website_data=website_data,
                db=db,
            )
            return website
    except WebsitesNotExist:
        raise WebsitesNotExist()
    except Exception:
        raise UnhandledException()


@router.delete(
    "/v1/entity-management/entities/{entity_uuid}/websites/{website_uuid}/",
    response_model=s_websites.WebsiteDelReponse,
    status_code=status.HTTP_200_OK,
)
async def soft_del_website(
    request: Request,
    response: Response,
    entity_uuid: UUID4,
    website_uuid: UUID4,
    website_data: s_websites.WebsitesSoftDel,
    db: AsyncSession = Depends(get_db),
):

    try:
        async with db.begin():
            sys_user = await serv_session.validate_session(
                request=request, response=response, db=db
            )
            SetSys.sys_deleted_by(data=website_data, sys_user=sys_user)
            website = await serv_web_d.soft_del_website(
                entity_uuid=entity_uuid,
                website_uuid=website_uuid,
                website_data=website_data,
                db=db,
            )
            return website
    except WebsitesNotExist:
        raise WebsitesNotExist()
    except Exception:
        raise UnhandledException()
