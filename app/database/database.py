from contextlib import asynccontextmanager
from typing import List
from config import settings as set
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

# Connection string for database connection.
connection_string = f"{set.db_connector}://{set.db_usrnm}:{set.db_pwd}@{set.db_hst}:{set.db_port}/{set.db_nm}"

try:
    # Create asynchronous engine for the database connection.
    async_engine = create_async_engine(connection_string, echo=True)
    print("connection made asynchronously")
except:
    print("ConnectionError")

# Factory for creating asynchronous sessions with SQLAlchemy.
LocalAsyncSession = async_sessionmaker(
    bind=async_engine, class_=AsyncSession, expire_on_commit=False
)

# Base class for SQLAlchemy models.
Base = declarative_base()


async def init_db_tables(model: object):
    """
    Initializes database tables based on the provided model.

    This function creates all the tables defined in the SQLAlchemy model's `Base.metadata`.

    :param model: The SQLAlchemy model class that defines the table structure.
    :type model: object
    :return: None
    :raises: SQLAlchemy exceptions if there is an issue with creating tables.
    """
    async with async_engine.begin() as conn:
        await conn.run_sync(model.Base.metadata.create_all)


async def init_db_table_schema(schema: str):
    """
    Initializes a database schema if it does not already exist.

    This function checks if a schema exists, and if not, creates the schema in the database.

    :param schema: The name of the schema to create.
    :type schema: str
    :return: None
    :raises: SQLAlchemy exceptions if there is an issue with schema creation.
    """
    async with async_engine.begin() as conn:
        stm = f"create schema if not exists {schema};"
        await conn.execute(text(stm))
        await conn.commit()


async def init_db_table_schema_factory(schemas: List[str]):
    """
    Initializes multiple database schemas.

    This function iterates over a list of schema names and creates each schema if it does not exist.

    :param schemas: A list of schema names to create.
    :type schemas: List[str]
    :return: None
    :raises: SQLAlchemy exceptions if there is an issue with schema creation.
    """
    for schema in schemas:
        await init_db_table_schema(schema=schema)


async def get_db():
    """
    Provides a session for database operations.

    This is an asynchronous generator that yields a database session object for use in operations,
    ensuring proper session closure when done.

    :return: The database session.
    :rtype: AsyncSession
    :raises: SQLAlchemy exceptions if there is an issue with session creation.
    """
    async with LocalAsyncSession() as db:
        try:
            yield db
        finally:
            await db.close()


@asynccontextmanager
async def transaction_manager(db: AsyncSession):
    """
    Manages database transactions for a given session.

    This context manager starts a transaction, yields the session for use in operations,
    and commits or rolls back the transaction depending on the outcome.

    :param db: The database session to manage transactions.
    :type db: AsyncSession
    :yield: The database session to use for performing transactions.
    :rtype: AsyncSession
    :raises: SQLAlchemy exceptions if there is an issue with transaction management.
    """
    async with db.begin():
        yield db
