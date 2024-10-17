from typing import Annotated, Literal, Optional

from fastapi import Depends, HTTPException, dependencies, status
from pydantic import UUID4
from sqlalchemy import Select, Update, and_
from sqlalchemy.ext.asyncio import AsyncSession

import app.constants as cnst
import app.models.websites as m_websites
import app.schemas.websites as s_websites
from app.database.database import Operations, get_db
from app.services.utilities import DataUtils as di


class WebsitesModels:
    websites = m_websites.Websites


class WebsitesStatements:
    pass

    class SelStatements:
        pass

        @staticmethod
        def sel_web_by_entity_web_uuid_stm(
            entity_uuid: UUID4,
            website_uuid: UUID4,
        ):
            websites = WebsitesModels.websites
            statement = Select(websites).where(
                and_(
                    websites.entity_uuid == entity_uuid,
                    websites.uuid == website_uuid,
                )
            )
            return statement

        @staticmethod
        def sel_web_entity_web_name_stm(
            entity_uuid: UUID4,
            website_name: str,
            db: AsyncSession = Depends(get_db),
        ):
            websites = WebsitesModels.websites
            statement = Select(websites).where(
                and_(
                    websites.entity_uuid == entity_uuid,
                    websites.url == website_name,
                )
            )

            return statement

    class UpdateStatements:
        pass

        @staticmethod
        def update_web_stm(
            entity_uuid: UUID4, website_uuid: UUID4, website_data: object
        ):
            websites = WebsitesModels.websites
            statement = (
                Update(websites)
                .where(
                    websites.entity_uuid == entity_uuid,
                    websites.uuid == website_uuid,
                )
                .values(di.set_empty_strs_null(website_data))
                .returning(websites)
            )
            return statement


class WebsitesServices:
    pass

    class ReadService:
        def __init__(self) -> None:
            pass

        async def get_website(
            self,
            entity_uuid: UUID4,
            website_uuid: UUID4,
            db: AsyncSession = Depends(get_db),
        ):

            statement = statement.sel_web_by_entity_web_uuid_stm(
                entity_uuid=entity_uuid, website_uuid=website_uuid
            )
            website = await Operations.return_one_row(
                service=cnst.WEBSITES_READ_SERVICE, statement=statement, db=db
            )
            di.rec_not_exist_or_soft_del(website)
            return website

    class CreateService:
        def __init__(self) -> None:
            pass

        async def create_website(
            self,
            website_data: s_websites.WebsitesCreate,
            db: AsyncSession = Depends(get_db),
        ):

            statement = WebsitesStatements.SelStatements.sel_web_entity_web_name_stm(
                entity_uuid=website_data.entity_uuid, website_name=website_data.url
            )
            websites = WebsitesModels.websites
            website_exists = await Operations.return_one_row(
                service=cnst.WEBSITES_CREATE_SERVICE, statement=statement, db=db
            )
            di.record_exists(model=website_exists)
            website = await Operations.add_instance(
                service=cnst.WEBSITES_CREATE_SERVICE,
                model=websites,
                data=website_data,
                db=db,
            )
            return website

    class UpdateService:
        def __init__(self) -> None:
            pass

        async def update_website_eng(
            self,
            entity_uuid: UUID4,
            website_uuid: UUID4,
            website_data: object,
            db: AsyncSession = Depends(get_db),
        ):

            statement = WebsitesStatements.UpdateStatements.update_web_stm(
                entity_uuid=entity_uuid,
                website_uuid=website_uuid,
                website_data=website_data,
            )
            website = await Operations.return_one_row(
                service=cnst.WEBSITES_UPDATE_SERVICE, statement=statement, db=db
            )
            di.rec_not_exist_or_soft_del(website)
            return website

    class DelService:
        def __init__(self) -> None:
            pass

        async def soft_del_website(
            self,
            entity_uuid: UUID4,
            website_uuid: UUID4,
            website_data: s_websites.WebsitesSoftDel,
            db: AsyncSession = Depends(get_db),
        ):

            statement = WebsitesStatements.UpdateStatements.update_web_stm(
                entity_uuid=entity_uuid,
                website_uuid=website_uuid,
                website_data=website_data,
            )
            website = await Operations.return_one_row(
                service=cnst.WEBSITES_DEL_SERVICE, statement=statement, db=db
            )
            return website
