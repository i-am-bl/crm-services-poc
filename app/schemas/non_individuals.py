from datetime import datetime
from typing import Optional

from pydantic import UUID4, BaseModel

from ._variables import ConstrainedStr, TimeStamp


class NonIndividuals(BaseModel):
    name: ConstrainedStr
    legal_name: Optional[ConstrainedStr] = None


class NonIndividualsCreate(NonIndividuals):
    entity_uuid: UUID4
    sys_created_by: Optional[UUID4] = None
    sys_created_at: datetime = TimeStamp


class NonIndividualsUpdate(BaseModel):
    name: Optional[ConstrainedStr] = None
    legal_name: Optional[ConstrainedStr] = None
    sys_updated_at: datetime = TimeStamp
    sys_updated_by: Optional[UUID4] = None


class NonIndividualsDel(BaseModel):
    sys_deleted_at: datetime = TimeStamp
    sys_deleted_by: Optional[UUID4] = None


class NonIndividualsResponse(BaseModel):
    # id: int
    uuid: UUID4
    # entity_uuid: UUID4
    name: ConstrainedStr
    legal_name: Optional[ConstrainedStr] = None
    sys_created_at: datetime
    sys_created_by: Optional[UUID4] = None
    sys_updated_at: Optional[datetime] = None
    sys_updated_by: Optional[UUID4] = None

    class Config:
        from_attributes = True


class NonIndividualsDelResponse(NonIndividualsResponse):
    sys_deleted_at: datetime
    sys_deleted_by: Optional[UUID4] = None

    class Config:
        from_attributes = True
