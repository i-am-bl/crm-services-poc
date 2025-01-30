from contextlib import asynccontextmanager
from typing import Annotated, List

from config import settings as set
from fastapi import Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base
from typing_extensions import Doc

from ..utilities.logger import logger
from ..utilities.utilities import DataUtils as di

connection_string = f"{set.db_connector}://{set.db_usrnm}:{set.db_pwd}@{set.db_hst}:{set.db_port}/{set.db_nm}"

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


@asynccontextmanager
async def transaction_manager(db: AsyncSession):
    async with db.begin():
        yield db
