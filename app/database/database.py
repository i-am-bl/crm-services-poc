from typing import List

from fastapi import Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

from config import settings as set
from app.logger import logger
from app.services.utilities import DataUtils as di

schema = "fastapi6"
connection_string = f"{set.db_connector}://{set.db_usrnm}:{set.db_pwd}@{set.db_hst}:{set.db_port}/{set.db_nm}"

print(connection_string)


try:
    async_engine = create_async_engine(connection_string, echo=True)
    print("connection made asyncronously")
except:
    print("ConnectionError")

LocalAsyncSession = async_sessionmaker(
    bind=async_engine, class_=AsyncSession, expire_on_commit=False
)

Base = declarative_base()


async def init_db_tables(model: object):
    async with async_engine.begin() as conn:
        await conn.run_sync(model.Base.metadata.create_all)


async def init_db_table_schema(schema: str):
    async with async_engine.begin() as conn:
        stm = f"create schema if not exists {schema};"
        await conn.execute(text(stm))
        await conn.commit()


async def init_db_table_schema_factory(schemas: List[str]):
    for schema in schemas:
        await init_db_table_schema(schema=schema)


async def get_db():
    async with LocalAsyncSession() as db:
        try:
            yield db
        finally:
            await db.close()


class Operations:
    @staticmethod
    async def return_one_row(
        service: str,
        statement: object,
        db: AsyncSession = Depends(get_db),
    ):
        logger.info({"statement": str(statement)})
        result = await db.execute(statement=statement)
        logger.info(f"Executing database operation for sevice: {service}.")
        entry = result.scalars().first()
        return entry

    @staticmethod
    async def return_all_rows(
        service: str,
        statement: object,
        db: AsyncSession = Depends(get_db),
    ):
        logger.info({"statement": str(statement)})
        result = await db.execute(statement=statement)
        logger.info(f"Executing database operation for sevice: {service}.")
        entry = result.scalars().all()
        return entry

    @staticmethod
    async def return_count(
        service: str,
        statement: object,
        db: AsyncSession = Depends(get_db),
    ):
        logger.info({"statement": str(statement)})
        result = await db.execute(statement=statement)
        logger.info(f"Executing database operation for sevice: {service}.")
        entry = result.scalar()
        return entry

    @staticmethod
    async def add_instance(
        service: str,
        model: object,
        data: object,
        db: AsyncSession = Depends(get_db),
    ):
        logger.info("Dumping data into model.")
        instance = model(**di.m_dumps(data=data))
        db.add(instance=instance)
        logger.info(f"Committing entry to the database for service: {service}.")
        return instance

    @staticmethod
    async def add_instances(
        service: str,
        model: object,
        data: object,
        db: AsyncSession = Depends(get_db),
    ):
        logger.info("Dumping data into model.")
        instances = [model(**di.m_dumps(instance)) for instance in data]
        db.add_all(instances=instances)
        logger.info(f"Committing entry to the database for service: {service}.")
        return instances
