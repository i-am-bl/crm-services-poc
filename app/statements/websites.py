from pydantic import UUID4
from sqlalchemy import Select, Update, and_, func
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.websites import Websites

from ..utilities.utilities import DataUtils as di


class WebsitesStms:
    def __init__(self, model: Websites) -> Select:
        self._model: Websites = model

    @property
    def model(self) -> Websites:
        return self._model

    def get_website(
        self,
        entity_uuid: UUID4,
        website_uuid: UUID4,
    ) -> Select:
        websites = self._model
        return Select(websites).where(
            and_(
                websites.entity_uuid == entity_uuid,
                websites.uuid == website_uuid,
                websites.sys_deleted_at == None,
            )
        )

    def get_websites(self, entity_uuid: UUID4, offset: int, limit: int) -> Select:
        websites = self._model
        return (
            Select(websites)
            .where(
                and_(
                    websites.entity_uuid == entity_uuid,
                    websites.sys_deleted_at == None,
                )
            )
            .offset(offset=offset)
            .limit(limit=limit)
        )
        return statement

    def get_websites_ct(
        self,
        entity_uuid: UUID4,
    ) -> Select:
        websites = self._model
        return (
            Select(func.count())
            .select_from(websites)
            .where(
                and_(
                    websites.entity_uuid == entity_uuid,
                    websites.sys_deleted_at == None,
                )
            )
        )

    def get_website_by_url(
        self,
        entity_uuid: UUID4,
        website_name: str,
        db: AsyncSession,
    ) -> Select:
        websites = self._model
        return Select(websites).where(
            and_(
                websites.entity_uuid == entity_uuid,
                websites.url == website_name,
                websites.sys_deleted_at == None,
            )
        )

    def update_website(
        self, entity_uuid: UUID4, website_uuid: UUID4, website_data: object
    ) -> Update:
        websites = self._model
        return (
            Update(websites)
            .where(
                websites.entity_uuid == entity_uuid,
                websites.uuid == website_uuid,
                websites.sys_deleted_at == None,
            )
            .values(di.set_empty_strs_null(website_data))
            .returning(websites)
        )
