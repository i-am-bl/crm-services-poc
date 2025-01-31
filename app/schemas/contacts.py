from datetime import datetime
from typing import Optional

from pydantic import UUID4, BaseModel


class ContactsBase(BaseModel):
    parent_uuid: UUID4
    child_uuid: UUID4


class ContactsCreate(ContactsBase): ...


class ContactsReturn(ContactsBase):
    id: int
    uuid: UUID4
    sys_created_at: datetime
    sys_updated_at: Optional[datetime]
