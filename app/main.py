from contextlib import asynccontextmanager

from fastapi import FastAPI
from pydantic import UUID4

from . import models
from .constants import constants as cnst
from .constants.handlers import handlers
from .database.database import init_db_table_schema_factory, init_db_tables
from .handlers.handler import handle_exeception_registration
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
handle_exeception_registration(app=app, handlers=handlers)

# app.include_router()
