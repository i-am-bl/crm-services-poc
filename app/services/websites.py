from typing import List
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from ..constants import constants as cnst
from ..database.operations import Operations
from ..exceptions import WebsitesExists, WebsitesNotExist
from ..models.websites import Websites
from ..schemas.websites import (
    WebsiteDelRes,
    WebsitesInternalCreate,
    WebsitesPgRes,
    WebsitesRes,
    WebsitesDel,
    WebsitesInternalUpdate,
)
from ..statements.websites import WebsitesStms
from ..utilities import pagination
from ..utilities.data import record_exists, record_not_exist


class ReadSrvc:
    """
    Service for reading and fetching website-related data from the database.

    This service provides methods for fetching websites, getting the count of websites,
    and paginating website results for an entity, using the provided database operations
    and statements.

    :param statements: A collection of statements for querying websites.
    :type statements: WebsitesStms
    :param db_operations: A collection of operations for performing database queries.
    :type db_operations: Operations
    """

    def __init__(self, statements: WebsitesStms, db_operations: Operations) -> None:
        """
        Initializes the ReadSrvc class with the provided statements and database operations.

        :param statements: A collection of statements for querying websites.
        :type statements: WebsitesStms
        :param db_operations: A collection of operations for performing database queries.
        :type db_operations: Operations
        """
        self._statements: WebsitesStms = statements
        self._db_ops: Operations = db_operations

    @property
    def statements(self) -> WebsitesStms:
        """
        Returns the instance of WebsitesStms.

        :returns: The statement service for querying websites.
        :rtype: WebsitesStms
        """
        return self._statements

    @property
    def db_operations(self) -> Operations:
        """
        Returns the instance of Operations.

        :returns: The database operation service for executing queries.
        :rtype: Operations
        """
        return self._db_ops

    async def get_website(
        self,
        entity_uuid: UUID4,
        website_uuid: UUID4,
        db: AsyncSession,
    ) -> WebsitesRes:
        """
        Retrieves a single website record by its UUID for a given entity.

        :param entity_uuid: The UUID of the entity owning the website.
        :type entity_uuid: UUID4
        :param website_uuid: The UUID of the website to be fetched.
        :type website_uuid: UUID4
        :param db: The asynchronous database session for querying.
        :type db: AsyncSession
        :returns: The website details.
        :rtype: WebsitesRes
        :raises: WebsitesNotExist if the website is not found.
        """
        statement = self._statements.get_website(
            entity_uuid=entity_uuid, website_uuid=website_uuid
        )
        website: WebsitesRes = await self._db_ops.return_one_row(
            service=cnst.WEBSITES_READ_SERVICE, statement=statement, db=db
        )
        return record_not_exist(instance=website, exception=WebsitesNotExist)

    async def get_websites(
        self,
        entity_uuid: UUID4,
        offset: int,
        limit: int,
        db: AsyncSession,
    ) -> List[WebsitesRes]:
        """
        Retrieves a list of websites for a given entity, with pagination support.

        :param entity_uuid: The UUID of the entity owning the websites.
        :type entity_uuid: UUID4
        :param offset: The starting point for fetching websites.
        :type offset: int
        :param limit: The number of websites to fetch.
        :type limit: int
        :param db: The asynchronous database session for querying.
        :type db: AsyncSession
        :returns: A list of website details.
        :rtype: List[WebsitesRes]
        :raises: WebsitesNotExist if no websites are found for the entity.
        """
        statement = self._statements.get_websites(
            entity_uuid=entity_uuid, offset=offset, limit=limit
        )
        websites: List[WebsitesRes] = await self._db_ops.return_all_rows(
            service=cnst.WEBSITES_READ_SERVICE, statement=statement, db=db
        )
        return record_not_exist(instance=websites, exception=WebsitesNotExist)

    async def get_websites_ct(
        self,
        entity_uuid: UUID4,
        db: AsyncSession,
    ) -> int:
        """
        Retrieves the count of websites for a given entity.

        :param entity_uuid: The UUID of the entity whose website count is to be fetched.
        :type entity_uuid: UUID4
        :param db: The asynchronous database session for querying.
        :type db: AsyncSession
        :returns: The total count of websites for the entity.
        :rtype: int
        """
        statement = self._statements.get_websites_ct(entity_uuid=entity_uuid)
        return await self._db_ops.return_count(
            service=cnst.WEBSITES_READ_SERVICE, statement=statement, db=db
        )

    async def paginated_websites(
        self, entity_uuid: UUID4, page: int, limit: int, db: AsyncSession
    ) -> WebsitesPgRes:
        """
        Retrieves a paginated list of websites for an entity, including metadata
        like total count, current page, and whether more websites are available.

        :param entity_uuid: The UUID of the entity whose websites are to be fetched.
        :type entity_uuid: UUID4
        :param page: The current page for pagination.
        :type page: int
        :param limit: The number of websites to fetch per page.
        :type limit: int
        :param db: The asynchronous database session for querying.
        :type db: AsyncSession
        :returns: A paginated result with metadata about the total number of websites,
                  current page, and list of websites for that page.
        :rtype: WebsitesPgRes
        """
        total_count = self.get_websites_ct(db=db)
        offset = pagination.page_offset(page=page, limit=limit)
        has_more = pagination.has_more_items(
            total_count=total_count, page=page, limit=limit
        )
        websites = await self.get_websites(
            entity_uuid=entity_uuid, offset=offset, limit=limit, db=db
        )
        return WebsitesPgRes(
            total=total_count,
            page=page,
            has_more=has_more,
            limit=limit,
            websites=websites,
        )


class CreateSrvc:
    """
    Service for creating and adding websites to the database.

    This service provides methods for checking the existence of a website based on URL,
    and for creating a new website record in the database.

    :param statements: A collection of statements for querying websites.
    :type statements: WebsitesStms
    :param db_operations: A collection of operations for performing database queries.
    :type db_operations: Operations
    :param model: The model representing a website entity in the database.
    :type model: Websites
    """

    def __init__(
        self, statements: WebsitesStms, db_operations: Operations, model: Websites
    ) -> None:
        """
        Initializes the CreateSrvc class with the provided statements, database operations,
        and the website model.

        :param statements: A collection of statements for querying websites.
        :type statements: WebsitesStms
        :param db_operations: A collection of operations for performing database queries.
        :type db_operations: Operations
        :param model: The model representing the website entity.
        :type model: Websites
        """
        self._statements: WebsitesStms = statements
        self._db_ops: Operations = db_operations
        self._model: Websites = model

    @property
    def statements(self) -> WebsitesStms:
        """
        Returns the instance of WebsitesStms for querying websites.

        :returns: The statement service for querying websites.
        :rtype: WebsitesStms
        """
        return self._statements

    @property
    def db_operations(self) -> Operations:
        """
        Returns the instance of Operations for executing database operations.

        :returns: The database operation service for executing queries.
        :rtype: Operations
        """
        return self._db_ops

    @property
    def model(self) -> Websites:
        """
        Returns the model representing a website entity in the database.

        :returns: The model for a website.
        :rtype: Websites
        """
        return self._model

    async def create_website(
        self,
        website_data: WebsitesInternalCreate,
        db: AsyncSession,
    ) -> WebsitesRes:
        """
        Creates a new website record in the database. First, checks if a website with
        the same URL already exists. If it does, an exception is raised. If it does not,
        the website is created.

        :param website_data: The data for the new website to be created.
        :type website_data: WebsitesInternalCreate
        :param db: The asynchronous database session to execute queries.
        :type db: AsyncSession
        :returns: The created website data.
        :rtype: WebsitesRes
        :raises: WebsitesExists if a website with the same URL already exists.
        :raises: WebsitesNotExist if the website creation fails or the website does not exist.
        """
        statement = self._statements.get_website_by_url(
            entity_uuid=website_data.entity_uuid, website_name=website_data.url
        )
        websites = self._model
        website_exists = await self._db_ops.return_one_row(
            service=cnst.WEBSITES_CREATE_SERVICE, statement=statement, db=db
        )
        record_exists(instance=website_exists, exception=WebsitesExists)

        website: WebsitesRes = await self._db_ops.add_instance(
            service=cnst.WEBSITES_CREATE_SERVICE,
            model=websites,
            data=website_data,
            db=db,
        )
        return record_not_exist(instance=website, exception=WebsitesNotExist)


class UpdateSrvc:
    """
    Service for updating existing websites in the database.

    This service provides methods for updating website information based on the given
    entity and website UUIDs. It ensures that the website exists before attempting to update
    it in the database.

    :param statements: A collection of statements for querying and updating websites.
    :type statements: WebsitesStms
    :param db_operations: A collection of operations for performing database queries.
    :type db_operations: Operations
    """

    def __init__(self, statements: WebsitesStms, db_operations: Operations) -> None:
        """
        Initializes the UpdateSrvc class with the provided statements and database operations.

        :param statements: A collection of statements for querying and updating websites.
        :type statements: WebsitesStms
        :param db_operations: A collection of operations for performing database queries.
        :type db_operations: Operations
        """
        self._statements: WebsitesStms = statements
        self._db_ops: Operations = db_operations

    @property
    def statements(self) -> WebsitesStms:
        """
        Returns the instance of WebsitesStms for querying and updating websites.

        :returns: The statement service for querying and updating websites.
        :rtype: WebsitesStms
        """
        return self._statements

    @property
    def db_operations(self) -> Operations:
        """
        Returns the instance of Operations for executing database operations.

        :returns: The database operation service for executing queries.
        :rtype: Operations
        """
        return self._db_ops

    async def update_website(
        self,
        entity_uuid: UUID4,
        website_uuid: UUID4,
        website_data: WebsitesInternalUpdate,
        db: AsyncSession,
    ) -> WebsitesRes:
        """
        Updates the website record in the database with the provided data. The method
        first checks if the website exists using the given entity and website UUIDs. If the
        website exists, it updates the record with the new data.

        :param entity_uuid: The UUID of the entity to which the website belongs.
        :type entity_uuid: UUID4
        :param website_uuid: The UUID of the website to be updated.
        :type website_uuid: UUID4
        :param website_data: The updated website data.
        :type website_data: WebsitesInternalUpdate
        :param db: The asynchronous database session to execute queries.
        :type db: AsyncSession
        :returns: The updated website data.
        :rtype: WebsitesRes
        :raises: WebsitesNotExist if the website does not exist.
        """
        statement = self._statements.update_website(
            entity_uuid=entity_uuid,
            website_uuid=website_uuid,
            website_data=website_data,
        )
        website: WebsitesRes = await self._db_ops.return_one_row(
            service=cnst.WEBSITES_UPDATE_SERVICE, statement=statement, db=db
        )
        return record_not_exist(instance=website, exception=WebsitesNotExist)


class DelSrvc:
    """
    Service for soft-deleting websites from the database.

    This service provides a method for marking a website as deleted in the database,
    ensuring that the website exists before performing the operation.

    :param statements: A collection of statements for querying and updating website data.
    :type statements: WebsitesStms
    :param db_operations: A collection of operations for performing database queries.
    :type db_operations: Operations
    """

    def __init__(self, statements: WebsitesStms, db_operations: Operations) -> None:
        """
        Initializes the DelSrvc class with the provided statements and database operations.

        :param statements: A collection of statements for querying and updating website data.
        :type statements: WebsitesStms
        :param db_operations: A collection of operations for performing database queries.
        :type db_operations: Operations
        """
        self._statements: WebsitesStms = statements
        self._db_ops: Operations = db_operations

    @property
    def statements(self) -> WebsitesStms:
        """
        Returns the instance of WebsitesStms for querying and updating website data.

        :returns: The statement service for querying and updating websites.
        :rtype: WebsitesStms
        """
        return self._statements

    @property
    def db_operations(self) -> Operations:
        """
        Returns the instance of Operations for executing database operations.

        :returns: The database operation service for executing queries.
        :rtype: Operations
        """
        return self._db_ops

    async def soft_del_website(
        self,
        entity_uuid: UUID4,
        website_uuid: UUID4,
        website_data: WebsitesDel,
        db: AsyncSession,
    ) -> WebsiteDelRes:
        """
        Soft deletes the website by updating its record in the database to mark it as deleted.
        The method first checks if the website exists using the given entity and website UUIDs,
        and if it exists, marks it as deleted.

        :param entity_uuid: The UUID of the entity to which the website belongs.
        :type entity_uuid: UUID4
        :param website_uuid: The UUID of the website to be deleted.
        :type website_uuid: UUID4
        :param website_data: The data to mark the website as deleted.
        :type website_data: WebsitesDel
        :param db: The asynchronous database session to execute queries.
        :type db: AsyncSession
        :returns: The result of the soft delete operation (updated website data).
        :rtype: WebsiteDelRes
        :raises: WebsitesNotExist if the website does not exist.
        """
        statement = self._statements.update_web(
            entity_uuid=entity_uuid,
            website_uuid=website_uuid,
            website_data=website_data,
        )
        website: WebsiteDelRes = await self._db_ops.return_one_row(
            service=cnst.WEBSITES_DEL_SERVICE, statement=statement, db=db
        )
        return record_not_exist(instance=website, exception=WebsitesNotExist)
