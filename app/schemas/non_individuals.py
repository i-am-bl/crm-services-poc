from datetime import datetime
from typing import Optional

from pydantic import UUID4, BaseModel

from app.schemas._variables import ConstrainedStr, TimeStamp


class NonIndividuals(BaseModel):
    name: ConstrainedStr
    legal_name: Optional[ConstrainedStr] = None


class NonIndividualsCreate(NonIndividuals):
    entity_id: int
    entity_uuid: UUID4


class NonIndividualsUpdate(BaseModel):
    name: Optional[ConstrainedStr] = None
    legal_name: Optional[ConstrainedStr] = None
    sys_updated_at: datetime = TimeStamp
    sys_updated_by: Optional[int] = None


class NonIndividualsDel(BaseModel):
    sys_deleted_at: datetime = TimeStamp
    sys_deleted_by: Optional[int] = None


class NonIndividualsResponse(BaseModel):
    id: int
    uuid: UUID4
    entity_id: int
    entity_uuid: UUID4
    name: ConstrainedStr
    legal_name: Optional[ConstrainedStr] = None
    sys_created_at: datetime
    sys_created_by: Optional[int] = None
    sys_updated_at: Optional[datetime] = None
    sys_updated_by: Optional[int] = None

    class Config:
        from_attributes = True


class NonIndividualsDelResponse(NonIndividualsResponse):
    sys_deleted_at: datetime
    sys_deleted_by: Optional[int] = None

    class Config:
        from_attributes = True
