from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_connector: str
    db_usrnm: str
    db_pwd: str
    db_hst: str
    db_port: str
    db_nm: str
    jwt_secret_key: str
    jwt_algorithm: str
    jwt_expiration: int

    class Config:
        env_file = ".env"


settings = Settings()
