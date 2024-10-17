from datetime import datetime
from typing import List, Optional

from click import Option
from pydantic import UUID4, BaseModel

from app.schemas._variables import ConstrainedStr, TimeStamp


class Individuals(BaseModel):
    first_name: ConstrainedStr
    last_name: Optional[ConstrainedStr] = None


class IndividualsCreate(Individuals):
    entity_id: int
    entity_uuid: UUID4


class IndividualsUpdate(BaseModel):
    first_name: Optional[ConstrainedStr] = None
    last_name: Optional[ConstrainedStr] = None
    sys_updated_at: datetime = TimeStamp
    sys_updated_by: Optional[int] = None


class IndividualsDel(BaseModel):
    sys_deleted_at: datetime = TimeStamp
    sys_deleted_by: Optional[int] = None


class IndividualsResponse(BaseModel):
    id: int
    uuid: UUID4
    first_name: Optional[ConstrainedStr] = None
    last_name: Optional[ConstrainedStr] = None
    sys_created_at: datetime
    sys_created_by: Optional[int] = None
    sys_updated_at: Optional[datetime] = None
    sys_updated_by: Optional[int] = None

    class Config:
        from_attributes = True


class IndividualsPagResponse(BaseModel):
    total: int
    page: int
    liimt: int
    has_more: bool
    individuals: Optional[List[IndividualsResponse]] = None


class IndividualsDelResponse(IndividualsResponse):
    sys_deleted_at: datetime
    sys_deleted_by: Optional[int] = None

    class Config:
        from_attributes = True
