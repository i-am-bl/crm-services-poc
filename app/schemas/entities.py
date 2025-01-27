from datetime import datetime
from token import OP
from typing import Annotated, List, Optional

from pydantic import UUID4, BaseModel

from ..constants.enums import EntityTypes
from ._variables import TimeStamp
from .individuals import IndividualsDelRes, IndividualsRes
from .non_individuals import NonIndividualsDelRes, NonIndividualsRes


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


class EntitiesRes(Entities):
    id: int
    uuid: UUID4
    sys_created_at: datetime
    sys_created_by: Optional[UUID4] = None
    sys_updated_at: Optional[datetime] = None
    sys_updated_by: Optional[UUID4] = None

    class Config:
        from_attributes = True


class IndividualNonIndividualRes(BaseModel):
    entity_uuid: Optional[UUID4] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    company_name: Optional[str] = None

    class Config:
        from_attributes = True


class EntitiesIndividualRes(Entities):
    id: int
    uuid: UUID4
    information: IndividualsRes
    sys_created_at: datetime
    sys_created_by: Optional[UUID4] = None
    sys_updated_at: Optional[datetime] = None
    sys_updated_by: Optional[UUID4] = None

    class Config:
        from_attributes = True


class EntitiesCombinedRes(BaseModel):
    entity: Optional[EntitiesRes] = None
    individual: Optional[IndividualsRes] = None
    non_individual: Optional[NonIndividualsRes] = None


class EntitiesPgRes(BaseModel):
    total: int
    page: int
    limit: int
    has_more: bool
    individuals: Optional[List[IndividualsRes]] = None
    non_individuals: Optional[List[NonIndividualsRes]] = None


class EntitiesDelRes(EntitiesRes):
    sys_deleted_at: datetime = TimeStamp
    sys_deleted_by: Optional[UUID4] = None

    class Config:
        from_attributes = True


class EntitiesCombinedDelRes(BaseModel):
    entity: Optional[EntitiesDelRes] = None
    individual: Optional[IndividualsDelRes] = None
    non_individual: Optional[NonIndividualsDelRes] = None
