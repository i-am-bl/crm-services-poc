from datetime import datetime
from typing import Annotated, Literal, Optional, List

from pydantic import UUID4, BaseModel

import app.constants as cnst
from app.schemas._variables import TimeStamp


class Entities(BaseModel):
    type: Annotated[str, Literal[cnst.ENTITY_INDIVIDUAL, cnst.ENTITY_NON_INDIVIDUAL]]


class EntitiesCreate(Entities):

    class Config:
        from_attributes = True


class EntitiesUpdate(BaseModel):
    type: Annotated[
        str, Optional[Literal[cnst.ENTITY_INDIVIDUAL, cnst.ENTITY_NON_INDIVIDUAL]]
    ] = None
    sys_updated_at: datetime = TimeStamp
    sys_updated_by: Optional[int] = None


class EntitiesDel(BaseModel):
    sys_deleted_at: datetime = TimeStamp
    sys_deleted_by: Optional[int] = None


class EntitiesResponse(Entities):
    id: int
    uuid: UUID4
    sys_created_at: datetime
    sys_created_by: Optional[int] = None
    sys_updated_at: Optional[datetime] = None
    sys_updated_by: Optional[int] = None

    class Config:
        from_attributes = True


class EntitiesPagResponse(BaseModel):
    total: int
    page: int
    limit: int
    has_more: bool
    entities: Optional[List[EntitiesResponse]] = None


class EntitiesDelResponse(EntitiesResponse):
    sys_deleted_at: datetime = TimeStamp
    sys_deleted_by: Optional[int] = None

    class Config:
        from_attributes = True
