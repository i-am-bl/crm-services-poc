from datetime import datetime
from token import OP
from typing import Annotated, List, Literal, Optional

from click import Option
from pydantic import UUID4, BaseModel

from ..constants.enums import EntityTypes
from ._variables import TimeStamp
from .individuals import IndividualsDelResponse, IndividualsResponse
from .non_individuals import NonIndividualsDelResponse, NonIndividualsResponse


class Entities(BaseModel):
    type: Annotated[EntityTypes, EntityTypes]


class EntitiesCreate(Entities):
    sys_created_at: datetime = TimeStamp
    sys_created_by: Optional[UUID4] = None


class EntitiesUpdate(BaseModel):
    type: Annotated[EntityTypes, EntityTypes]
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


class EntitiesIndivNonIndivResponse(BaseModel):
    entity_uuid: Optional[UUID4] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    company_name: Optional[str] = None

    class Config:
        from_attributes = True


class EntitiesIndivResponse(Entities):
    id: int
    uuid: UUID4
    information: IndividualsResponse
    sys_created_at: datetime
    sys_created_by: Optional[UUID4] = None
    sys_updated_at: Optional[datetime] = None
    sys_updated_by: Optional[UUID4] = None

    class Config:
        from_attributes = True


class EntitiesCombinedResponse(BaseModel):
    entity: Optional[EntitiesResponse] = None
    individual: Optional[IndividualsResponse] = None
    non_individual: Optional[NonIndividualsResponse] = None


class EntitiesPagResponse(BaseModel):
    total: int
    page: int
    limit: int
    has_more: bool
    individuals: Optional[List[IndividualsResponse]] = None
    non_individuals: Optional[List[NonIndividualsResponse]] = None


class EntitiesDelResponse(EntitiesResponse):
    sys_deleted_at: datetime = TimeStamp
    sys_deleted_by: Optional[UUID4] = None

    class Config:
        from_attributes = True


class EntitiesCombinedDelResponse(BaseModel):
    entity: Optional[EntitiesDelResponse] = None
    individual: Optional[IndividualsDelResponse] = None
    non_individual: Optional[NonIndividualsDelResponse] = None
