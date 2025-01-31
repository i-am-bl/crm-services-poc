from datetime import datetime
from pydantic import BaseModel, Field


class TokenRequest(BaseModel):
    """Represents a request for authentication.

    This model is used to submit user credentials for token generation.
    """

    username: str = Field(
        ..., description="Username of the user requesting authentication."
    )
    password: str = Field(..., description="Password associated with the user account.")


class Token(BaseModel):
    """Represents an authentication token response.

    Contains the access token and its type after a successful authentication.
    """

    access_token: str = Field(..., description="JWT access token issued to the user.")
    token_type: str = Field(..., description="Type of the token.")


class TokenData(BaseModel):
    """Represents decoded token data.

    Contains essential claims from the token, including subject and expiration time.
    """

    sub: str = Field(..., description="Subject of the token, user ID.")
    exp: datetime = Field(..., description="Expiration timestamp of the token.")

    class Config:
        from_attributes = True
