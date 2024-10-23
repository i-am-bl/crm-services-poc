from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import UUID4

from . import models
from .constants import constants as cnst
from .constants.error_handlers import handlers
from .constants.routers import routers
from .database.database import init_db_table_schema_factory, init_db_tables
from .handlers.handler import (handle_exeception_registration,
                               handle_router_registration)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db_table_schema_factory(schemas=cnst.SCHEMAS)
    await init_db_tables(model=models.base)
    yield


app = FastAPI(
    lifespan=lifespan,
    title="CRM",
    description="backend service for CRM",
    version="v1",
)

handle_router_registration(app=app, routers=routers)
handle_exeception_registration(app=app, handlers=handlers)
