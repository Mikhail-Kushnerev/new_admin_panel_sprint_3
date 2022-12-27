from pydantic import BaseSettings, Field


class PostgreSQL(BaseSettings):
    dbname: str = Field(..., env='POSTGRES_DB')
    user: str = Field(..., env='POSTGRES_USERNAME')
    password: str = Field(..., env='POSTGRES_PASSWORD')
    host: str = Field(..., env='POSTGRES_HOST')
    port: int = Field(..., env='POSTGRES_PORT')

    class Config:
        env_file = "../.env"
