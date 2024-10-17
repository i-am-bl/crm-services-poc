from datetime import datetime

from pydantic import BaseModel


class TokenRequest(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    sub: str
    exp: datetime

    class Config:
        from_attributes = True
