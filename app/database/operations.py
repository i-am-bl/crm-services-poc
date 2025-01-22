from sqlalchemy.ext.asyncio import AsyncSession

from ..utilities.logger import logger
from ..utilities.utilities import DataUtils as di


class Operations:
    """
    Class contains utilities that are specific to database interaction.
    """

    @staticmethod
    async def return_one_row(
        service: str,
        statement: object,
        db: AsyncSession,
    ):
        logger.info({"statement": str(statement)})
        logger.info(f"Executing database operation for sevice: {service}.")
        result = await db.execute(statement=statement)
        return result.scalars().first()

    @staticmethod
    async def return_all_rows(
        service: str,
        statement: object,
        db: AsyncSession,
    ):
        """
        Returns all rows when select * is used.
        """
        logger.info({"statement": str(statement)})
        logger.info(f"Executing database operation for sevice: {service}.")
        result = await db.execute(statement=statement)
        return result.scalars().all()

    @staticmethod
    async def return_all_rows_and_values(
        service: str,
        statement: object,
        db: AsyncSession,
    ):
        """
        Returns all rows and values when select * is NOT used.

        example: select column1, column2, ... from table
        """
        logger.info({"statement": str(statement)})
        logger.info(f"Executing database operation for sevice: {service}.")
        result = await db.execute(statement=statement)
        return result.all()

    @staticmethod
    async def return_count(
        service: str,
        statement: object,
        db: AsyncSession,
    ):
        """
        Returns one value.

        Specifically used for selecting count for pagination purposes.
        example: select count(1) from table
        """
        logger.info({"statement": str(statement)})
        logger.info(f"Executing database operation for sevice: {service}.")
        result = await db.execute(statement=statement)
        return result.scalar()

    @staticmethod
    async def add_instance(
        service: str,
        model: object,
        data: object,
        db: AsyncSession,
    ):
        """
        Commits one item or inserts one row to the database.
        """
        logger.info("Dumping data into model.")
        instance = model(**di.m_dumps(data=data))
        logger.info(f"Executing database operation for sevice: {service}.")
        db.add(instance=instance)
        logger.info(f"Committing entry to the database for service: {service}.")
        return instance

    @staticmethod
    async def add_instances(
        service: str,
        model: object,
        data: object,
        db: AsyncSession,
    ):
        """
        Commits many items or rows to the database.
        """
        logger.info("Dumping data into model.")
        instances = [model(**di.m_dumps(instance)) for instance in data]
        db.add_all(instances=instances)
        logger.info(f"Committing entry to the database for service: {service}.")
        return instances
