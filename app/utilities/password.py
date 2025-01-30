"""
Password utilities for handling password hashing and validation.
"""

from passlib.hash import pbkdf2_sha256
from pydantic import UUID4

from ..exceptions import InvalidCredentials


def create_hash(password: str) -> str:
    """
    Generates a hashed version of the provided password using pbkdf2_sha256 algorithm.

    :param password: str: The password to hash.
    :return: str: The hashed password.
    """
    return pbkdf2_sha256.hash(secret=password)


def validate_hash(password: str, hash: str) -> bool:
    """
    Validates if the provided password matches the stored hash.

    :param password: str: The plain-text password to verify.
    :param hash: str: The stored hashed password.
    :raises InvalidCredentials: If the password does not match the hash.
    :return: bool: True if the password matches the hash, raises InvalidCredentials otherwise.
    """
    if pbkdf2_sha256.verify(secret=password, hash=hash):
        return True
    raise InvalidCredentials()
