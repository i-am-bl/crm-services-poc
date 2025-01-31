from datetime import datetime
from typing import List, Optional
import re

from pydantic import UUID4, BaseModel, Field, field_validator

from ._variables import ConstrainedEmailStr, ConstrainedStr, TimeStamp


class SysUsers(BaseModel):
    """Model representing system user details."""

    first_name: ConstrainedStr = Field(..., description="The user's first name.")
    last_name: ConstrainedStr = Field(..., description="The user's last name.")
    email: ConstrainedEmailStr = Field(
        ...,
        description="The user's email address. Must meet standard email format criteria: e.g., my.email@domain.com.",
    )
    username: ConstrainedStr = Field(..., description="The user's username.")

    @field_validator("email")
    def normalize_email(cls, value):
        """Normalize email to lowercase."""
        return value.lower()

    @field_validator("username")
    def normalize_username(cls, value):
        """Normalize username to lowercase."""
        return value.lower()


class SysUsersCreate(SysUsers):
    """Model for creating a new system user."""

    password: ConstrainedStr = Field(
        ...,
        description="The user's password. It must meet the following criteria: \
            - At least 8 characters long \
            - No more than 30 characters long \
            - At least one lowercase letter, one uppercase letter, and one numerical character.",
    )
    sys_created_at: datetime = TimeStamp

    @field_validator("password")
    def validate_password(cls, value):
        """Validate the user's password against defined criteria."""
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long.")
        if len(value) > 30:
            raise ValueError("Password must be less than or equal to 30 characters.")
        if not re.search(r"[A-Z]", value):
            raise ValueError("Password must contain at least one uppercase letter.")
        if not re.search(r"[a-z]", value):
            raise ValueError("Password must contain at least one lowercase letter.")
        if not re.search(r"\d", value):
            raise ValueError("Password must contain at least one numerical character.")
        # Special characters validation can be added once unicode issues are resolved.
        return value


class SysUsersUpdate(BaseModel):
    """Model for updating an existing system user's details."""

    first_name: Optional[ConstrainedStr] = Field(
        None, description="The user's updated first name (optional)."
    )
    last_name: Optional[ConstrainedStr] = Field(
        None, description="The user's updated last name (optional)."
    )
    email: Optional[ConstrainedEmailStr] = Field(
        None, description="The user's updated email address (optional)."
    )
    username: Optional[ConstrainedStr] = Field(
        None, description="The user's updated username (optional)."
    )
    password: Optional[ConstrainedStr] = Field(
        None, description="The user's updated password (optional)."
    )

    @field_validator("password")
    def validate_password(cls, value):
        """Validate the updated password against defined criteria."""
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long.")
        if len(value) > 30:
            raise ValueError("Password must be less than or equal to 30 characters.")
        if not re.search(r"[A-Z]", value):
            raise ValueError("Password must contain at least one uppercase letter.")
        if not re.search(r"[a-z]", value):
            raise ValueError("Password must contain at least one lowercase letter.")
        if not re.search(r"\d", value):
            raise ValueError("Password must contain at least one numerical character.")
        # Special characters validation can be added once unicode issues are resolved.
        return value


class SysUsersInternalUpdate(SysUsersUpdate):
    """Model for updating an existing system user's details.

    Hides system level fields from client.
    """

    sys_updated_at: datetime = TimeStamp
    sys_updated_by: Optional[UUID4] = Field(
        None, description="The UUID of the user who updated the record."
    )


class SysUsersDel(BaseModel):
    """Model for deleting a system user."""

    sys_deleted_at: datetime = TimeStamp
    sys_deleted_by: Optional[UUID4] = Field(
        None, description="The UUID of the user who deleted the record."
    )


class SysUsersDisable(BaseModel):
    """Model for disabling a system user."""

    disabled_at: datetime = TimeStamp


class SysUsersRes(BaseModel):
    """Response model for system user details."""

    id: int = Field(..., description="The ID of the system user.")
    uuid: UUID4 = Field(..., description="The UUID of the system user.")
    first_name: ConstrainedStr = Field(..., description="The user's first name.")
    last_name: ConstrainedStr = Field(..., description="The user's last name.")
    email: ConstrainedEmailStr = Field(..., description="The user's email address.")
    username: ConstrainedStr = Field(..., description="The user's username.")
    sys_created_at: datetime = Field(
        ..., description="Timestamp when the user was created."
    )
    sys_created_by: Optional[UUID4] = Field(
        None, description="The UUID of the user who created the record."
    )
    sys_updated_at: Optional[datetime] = Field(
        None, description="Timestamp when the user was last updated."
    )
    sys_updated_by: Optional[UUID4] = Field(
        None, description="The UUID of the user who last updated the record."
    )

    class Config:
        from_attributes = True


class SysUsersPgRes(BaseModel):
    """Paginated response model for system users."""

    total: int = Field(..., description="Total number of system users.")
    page: int = Field(..., description="Current page number.")
    limit: int = Field(..., description="Maximum number of users per page.")
    has_more: bool = Field(
        ..., description="Indicates whether there are more pages available."
    )
    sys_users: Optional[List[SysUsersRes]] = Field(
        None, description="List of system users in the current page."
    )


class SysUsersDelRes(SysUsersRes):
    """Response model for deleted system users."""

    sys_deleted_at: datetime = Field(
        ..., description="Timestamp when the user was deleted."
    )
    sys_deleted_by: Optional[UUID4] = Field(
        None, description="The UUID of the user who deleted the record."
    )


class SysUserLogin(BaseModel):
    """Model for system user login credentials."""

    username: str = Field(..., description="The user's username.")
    password: str = Field(..., description="The user's password.")


class Token(BaseModel):
    """Model for authentication token."""

    access_token: str = Field(..., description="The access token for authentication.")
    token_type: str = Field(..., description="The type of the token (e.g., 'bearer').")


class TokenData(BaseModel):
    """Model for token data associated with a logged-in user."""

    sys_user_id: str = Field(..., description="The ID of the system user.")
    username: str = Field(..., description="The username of the system user.")
