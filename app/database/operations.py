from typing import Any, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Select, Update
from ..utilities.logger import logger
from ..utilities.data import m_dumps


class Operations:
    """
    Utility class for interacting with the database.

    This class provides static methods for common database operations such as
    fetching rows, counting rows, and inserting instances. It works asynchronously
    with SQLAlchemy's `AsyncSession`.

    ivars:
        ivar: _logger: A logger utility for logging database operations.
        varType: logger
        ivar: _m_dumps: A utility function for serializing data before inserting it into the model.
        varType: m_dumps
    """

    @staticmethod
    async def return_one_row(
        service: str,
        statement: Select | Update,
        db: AsyncSession,
    ) -> Any:
        """
        Executes a SQL statement and returns a single row.

        This method is used for queries expected to return a single row,
        fetching the result using `scalars().first()`.

        :param service: The name of the service requesting the operation.
        :type service: str
        :param statement: The SQL statement to execute. It can be a `Select` or `Update` statement.
        :type statement: Select | Update
        :param db: The database session.
        :type db: AsyncSession
        :return: The first row of the result or `None` if no rows are returned.
        :rtype: Any
        """
        logger.info({"statement": str(statement)})
        logger.info(f"Executing database operation for service: {service}.")
        result = await db.execute(statement=statement)
        return result.scalars().first()

    @staticmethod
    async def return_all_rows(
        service: str,
        statement: Select | Update,
        db: AsyncSession,
    ) -> List[Any]:
        """
        Executes a SQL statement and returns all rows when `SELECT *` is used.

        This method is used when the query is expected to return all columns
        from a table using `SELECT *`.

        :param service: The name of the service requesting the operation.
        :type service: str
        :param statement: The SQL statement to execute. It can be a `Select` or `Update` statement.
        :type statement: Select | Update
        :param db: The database session.
        :type db: AsyncSession
        :return: A list of all rows returned by the query.
        :rtype: List[Any]
        """
        logger.info({"statement": str(statement)})
        logger.info(f"Executing database operation for service: {service}.")
        result = await db.execute(statement=statement)
        return result.scalars().all()

    @staticmethod
    async def return_all_rows_and_values(
        service: str,
        statement: Select | Update,
        db: AsyncSession,
    ) -> List[tuple]:
        """
        Executes a SQL statement and returns all rows and values when `SELECT *` is not used.

        This method is used when specific columns are selected in the query,
        for example: `SELECT column1, column2 FROM table`.

        :param service: The name of the service requesting the operation.
        :type service: str
        :param statement: The SQL statement to execute. It can be a `Select` or `Update` statement.
        :type statement: Select | Update
        :param db: The database session.
        :type db: AsyncSession
        :return: A list of rows with their corresponding values.
        :rtype: List[tuple]
        """
        logger.info({"statement": str(statement)})
        logger.info(f"Executing database operation for service: {service}.")
        result = await db.execute(statement=statement)
        return result.all()

    @staticmethod
    async def return_count(
        service: str,
        statement: Select | Update,
        db: AsyncSession,
    ) -> int:
        """
        Executes a SQL statement and returns a count value (typically used for pagination).

        This method is specifically used to return a single value, like the
        result of `SELECT COUNT(*) FROM table`.

        :param service: The name of the service requesting the operation.
        :type service: str
        :param statement: The SQL statement to execute. It can be a `Select` or `Update` statement.
        :type statement: Select | Update
        :param db: The database session.
        :type db: AsyncSession
        :return: The count value returned by the query.
        :rtype: int
        """
        logger.info({"statement": str(statement)})
        logger.info(f"Executing database operation for service: {service}.")
        result = await db.execute(statement=statement)
        return result.scalar()

    @staticmethod
    async def add_instance(
        service: str,
        model: object,
        data: object,
        db: AsyncSession,
    ) -> object:
        """
        Inserts a single instance (row) into the database.

        This method commits one item into the database after dumping the data
        into the model.

        :param service: The name of the service requesting the operation.
        :type service: str
        :param model: The model class to insert the data into.
        :type model: object
        :param data: The data to insert into the model.
        :type data: object
        :param db: The database session.
        :type db: AsyncSession
        :return: The inserted instance.
        :rtype: object
        """
        logger.info("Dumping data into model.")
        instance = model(**m_dumps(data=data))
        logger.info(f"Executing database operation for service: {service}.")
        db.add(instance=instance)
        logger.info(f"Committing entry to the database for service: {service}.")
        return instance

    @staticmethod
    async def add_instances(
        service: str,
        model: object,
        data: object,
        db: AsyncSession,
    ) -> List[object]:
        """
        Inserts multiple instances (rows) into the database.

        This method commits many items into the database after dumping the data
        into the model.

        :param service: The name of the service requesting the operation.
        :type service: str
        :param model: The model class to insert the data into.
        :type model: object
        :param data: A list of data to insert into the model.
        :type data: object
        :param db: The database session.
        :type db: AsyncSession
        :return: A list of inserted instances.
        :rtype: List[object]
        """
        logger.info("Dumping data into model.")
        instances = [model(**m_dumps(instance)) for instance in data]
        db.add_all(instances=instances)
        logger.info(f"Committing entries to the database for service: {service}.")
        return instances
