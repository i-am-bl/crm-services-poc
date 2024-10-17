from contextlib import asynccontextmanager

from fastapi import FastAPI, status
from pydantic import UUID4

from . import models
from .constants import constants as cnst
from .database.database import (init_db_table_schema,
                                init_db_table_schema_factory, init_db_tables)
from .reg_handlers import register_exception_handlers
from .reg_routers import register_routers


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db_table_schema_factory(schemas=cnst.SCHEMAS)
    await init_db_tables(model=models.base)
    yield


app = FastAPI(
    lifespan=lifespan, title="CRM", description="backend service for CRM", version="v1"
)

register_routers(app=app)
register_exception_handlers(app=app)
