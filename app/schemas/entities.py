from datetime import datetime
from typing import Annotated, List, Literal, Optional

from pydantic import UUID4, BaseModel

from ..constants import constants as cnst
from ._variables import TimeStamp


class Entities(BaseModel):
    type: Annotated[str, Literal[cnst.ENTITY_INDIVIDUAL, cnst.ENTITY_NON_INDIVIDUAL]]


class EntitiesCreate(Entities):
    sys_created_at: datetime = TimeStamp
    sys_created_by: Optional[UUID4] = None


class EntitiesUpdate(BaseModel):
    type: Annotated[
        str, Optional[Literal[cnst.ENTITY_INDIVIDUAL, cnst.ENTITY_NON_INDIVIDUAL]]
    ] = None
    sys_updated_at: datetime = TimeStamp
    sys_updated_by: Optional[UUID4] = None


class EntitiesDel(BaseModel):
    sys_deleted_at: datetime = TimeStamp
    sys_deleted_by: Optional[UUID4] = None


class EntitiesResponse(Entities):
    id: int
    uuid: UUID4
    sys_created_at: datetime
    sys_created_by: Optional[UUID4] = None
    sys_updated_at: Optional[datetime] = None
    sys_updated_by: Optional[UUID4] = None

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
    sys_deleted_by: Optional[UUID4] = None

    class Config:
        from_attributes = True
