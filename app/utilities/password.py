from passlib.hash import pbkdf2_sha256
from pydantic import UUID4

from ..exceptions import InvalidCredentials


def create_hash(password: str):
    return pbkdf2_sha256.hash(secret=password)


def validate_hash(password: str, hash: str):
    if pbkdf2_sha256.verify(secret=password, hash=hash):
        return True
    raise InvalidCredentials()
