from typing import Optional
from uuid import UUID

from pydantic import BaseSettings, BaseModel, Field


class Model(BaseModel):
    id: UUID
    imdb_rating: float
    genre: list[str]
    title: str
    description: Optional[str]
    director: list[Optional[str]]
    actors_names: list[str]
    writers_names: list[str]
    actors: list[dict[str, str]]
    writers: list[dict[str, str]]


class PostgresConfig(BaseSettings):
    dbname: str = Field(..., env='POSTGRES_DB')
    user: str = Field(..., env='POSTGRES_USER')
    password: str = Field(..., env='POSTGRES_PASSWORD')
    host: str = Field(..., env='POSTGRES_HOST')
    port: int = Field(..., env='POSTGRES_PORT')

    class Config:
        env_file = "../.env"


class ElasticConfig(BaseSettings):
    host: str = Field(..., env='ELASTIC_HOST')
    port: int = Field(..., env='ELASTIC_PORT')

    def elastic_url(self):
        return 'http://{host}:{port}/'.format(host=self.host, port=self.port)

    class Config:
        env_file = '../.env'


postgres: PostgresConfig = PostgresConfig()
elastic: ElasticConfig = ElasticConfig()
