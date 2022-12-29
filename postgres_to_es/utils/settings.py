from pydantic import BaseSettings, Field


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


postgres = PostgresConfig()
elastic = ElasticConfig()
