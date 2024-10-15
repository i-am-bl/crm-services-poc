from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, dependencies, status
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

import app.constants as cnst
import app.schemas.websites as s_websites
from app.database.database import get_db
from app.services.websites import WebsitesServices

serv_web_c = WebsitesServices.CreateService()
serv_web_r = WebsitesServices.ReadService()
serv_web_u = WebsitesServices.UpdateService()
serv_web_d = WebsitesServices.DelService()


router = APIRouter()


@router.get(
    "/v1/entity-management/entities/{entity_uuid}/websites/{website_uuid}/",
    response_model=s_websites.WebsiteReponse,
    status_code=status.HTTP_200_OK,
)
async def get_website(
    entity_uuid: UUID4, website_uuid: UUID4, db: AsyncSession = Depends(get_db)
):
    """Retrieve single website by entity_uuid and website_uuid"""
    async with db.begin():
        website = await serv_web_r.get_website(
            entity_uuid=entity_uuid,
            website_uuid=website_uuid,
            db=db,
        )
    return website


@router.get(
    "/v1/entity-management/entities/{entity_uuid}/websites/",
    response_model=s_websites.WebsiteReponse,
    status_code=status.HTTP_200_OK,
)
async def get_website(
    entity_uuid: UUID4, website_uuid: UUID4, db: AsyncSession = Depends(get_db)
):
    """Retrieve all websites by entity_uuid"""
    async with db.begin():
        website = await serv_web_r.get_website(
            entity_uuid=entity_uuid,
            website_uuid=website_uuid,
            db=db,
        )
    return website


@router.post(
    "/v1/entity-management/entities/{entity_uuid}/websites/",
    response_model=s_websites.WebsiteReponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_website(
    website_data: s_websites.WebsitesCreate, db: AsyncSession = Depends(get_db)
):
    """Create a single entity website record."""
    async with db.begin():
        website = await serv_web_c.create_website(website_data=website_data, db=db)
        return website


@router.put(
    "/v1/entity-management/entities/{entity_uuid}/websites/{website_uuid}/",
    response_model=s_websites.WebsiteReponse,
    status_code=status.HTTP_200_OK,
)
async def update_website(
    entity_uuid: UUID4,
    website_uuid: UUID4,
    website_data: s_websites.WebsitesUpdate,
    db: AsyncSession = Depends(get_db),
):
    async with db.begin():
        website = await serv_web_u.update_website(
            entity_uuid=entity_uuid,
            website_uuid=website_uuid,
            website_data=website_data,
            db=db,
        )
        return website


@router.delete(
    "/v1/entity-management/entities/{entity_uuid}/websites/{website_uuid}/",
    response_model=s_websites.WebsiteDelReponse,
    status_code=status.HTTP_200_OK,
)
async def soft_del_website(
    entity_uuid: UUID4,
    website_uuid: UUID4,
    website_data: s_websites.WebsitesSoftDel,
    db: AsyncSession = Depends(get_db),
):

    async with db.begin():
        website = await serv_web_d.soft_del_website(
            entity_uuid=entity_uuid,
            website_uuid=website_uuid,
            website_data=website_data,
            db=db,
        )
        return website
