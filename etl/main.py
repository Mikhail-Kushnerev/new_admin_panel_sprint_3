from elasticsearch import Elasticsearch
from psycopg2 import connect
from psycopg2.extras import DictCursor


from load_data import Postgres, Elastic
from utils.constants import HOST, PORT
from utils.settings import PostgreSQL
from utils.storage import State, JsonFileStorage


def build_storage():
    state = State(JsonFileStorage('file_path.json'))
    return state


def load_datas_from_psql_to_es():
    obj, es, storage = PostgreSQL(), Elasticsearch(hosts=f'{HOST}:{PORT}'), build_storage()
    elastic = Elastic(es)
    with connect(**obj.dict(), cursor_factory=DictCursor) as pg_conn:
        postgres_datas = Postgres(pg_conn, storage)
        for data in postgres_datas():
            # print(data)
            elastic.create_body_documents(data)


def main():
    load_datas_from_psql_to_es()


if __name__ == '__main__':
    main()
