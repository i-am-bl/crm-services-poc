import bcrypt
from passlib.context import CryptContext
from passlib.hash import pbkdf2_sha256


class AuthUtils:
    def __init__(self) -> None: ...

    @staticmethod
    def gen_hash(password: str):
        return pbkdf2_sha256.hash(password)

    @staticmethod
    def validate_hash(password: str, hash: str):
        return pbkdf2_sha256.verify(password, hash)


def pagination_offset(page: int, limit: int) -> int:
    offset = (page - 1) * limit
    return offset
