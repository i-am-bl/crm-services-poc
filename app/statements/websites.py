from pydantic import UUID4
from sqlalchemy import Select, Update, and_, func
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.websites import Websites

from ..utilities.data import set_empty_strs_null


class WebsitesStms:
    """
    A class responsible for constructing SQLAlchemy queries and statements for managing websites.

    ivars:
    ivar: _model: Websites: An instance of the Websites model.
    """

    def __init__(self, model: Websites) -> None:
        """
        Initializes the WebsitesStms class.

        :param model: Websites: An instance of the Websites model.
        :return: None
        """
        self._model: Websites = model

    @property
    def model(self) -> Websites:
        """
        Returns the instance of the Websites model.

        :return: Websites: The Websites model instance.
        """
        return self._model

    def get_website(
        self,
        entity_uuid: UUID4,
        website_uuid: UUID4,
    ) -> Select:
        """
        Selects a website based on the provided entity and website UUIDs.

        :param entity_uuid: UUID4: The UUID of the entity associated with the website.
        :param website_uuid: UUID4: The UUID of the website.
        :return: Select: A Select statement for the website with the specified entity and website UUIDs.
        """
        websites = self._model
        return Select(websites).where(
            and_(
                websites.entity_uuid == entity_uuid,
                websites.uuid == website_uuid,
                websites.sys_deleted_at == None,
            )
        )

    def get_websites(self, entity_uuid: UUID4, offset: int, limit: int) -> Select:
        """
        Selects websites associated with the given entity UUID, with pagination support.

        :param entity_uuid: UUID4: The UUID of the entity to filter websites by.
        :param offset: int: The number of websites to skip.
        :param limit: int: The maximum number of websites to return.
        :return: Select: A Select statement for websites with the specified entity UUID and pagination.
        """
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

    def get_websites_ct(self, entity_uuid: UUID4) -> Select:
        """
        Selects the count of all websites associated with the given entity UUID.

        :param entity_uuid: UUID4: The UUID of the entity to count websites for.
        :return: Select: A Select statement for the count of websites with the specified entity UUID.
        """
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
        """
        Selects a website by its URL associated with the specified entity UUID.

        :param entity_uuid: UUID4: The UUID of the entity associated with the website.
        :param website_name: str: The URL of the website.
        :param db: AsyncSession: The database session for async operations (unused in the method but required).
        :return: Select: A Select statement for the website with the specified entity UUID and URL.
        """
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
        """
        Updates a website based on its entity UUID and website UUID with the provided data.

        :param entity_uuid: UUID4: The UUID of the entity associated with the website.
        :param website_uuid: UUID4: The UUID of the website to be updated.
        :param website_data: object: The data to update the website with.
        :return: Update: An Update statement for the website with the specified UUIDs and new data.
        """
        websites = self._model
        return (
            Update(websites)
            .where(
                websites.entity_uuid == entity_uuid,
                websites.uuid == website_uuid,
                websites.sys_deleted_at == None,
            )
            .values(set_empty_strs_null(website_data))
            .returning(websites)
        )
