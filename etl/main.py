from psycopg2 import connect
from psycopg2.extras import DictCursor


from load_data import Postgres
from utils.settings import PostgreSQL
from utils.storage import State, JsonFileStorage


def build_storage():
    state = State(JsonFileStorage('file_path.json'))
    return state


def load_datas_from_psql_to_es():
    obj, storage = PostgreSQL(), build_storage()
    with connect(**obj.dict(), cursor_factory=DictCursor) as pg_conn:
        postgres_datas = Postgres(pg_conn, storage)
        _, *end = postgres_datas()


def main():
    load_datas_from_psql_to_es()


if __name__ == '__main__':
    main()
    # es = Elasticsearch(hosts='http://localhost:9200/')

    # body = {
    #     "dynamic": "strict",
    #     "properties": {
    #             "imdb_rating": {
    #                 "type": "keyword"
    #             },
    #             "genre": {
    #                 "type": "keyword"
    #             }
    #         }
    #     }
    #
    # es.indices.create(index='csx', mappings=mappings, settings=settings)

    action = [{
        "_index": "csx",
        "_source": {
            "id": '123qwe',
            "imdb_rating": 1.62,
            "genre": ['Game-Show', 'Music', 'Reality-TV'],
            "title": "q",
            "description": "description",
            "director": "director",
            "writers_names": ['Cole S. McKay', 'Fred Olen Ray'],
            "actors_names": ['Cole S. McKay', 'Fred Olen Ray'],
            "actors": {
                "id": "123",
                "name": "name"
            },
            "writers": {
                "id": "123",
                "name": "name"
            }
        }
    }]

    # helpers.bulk(es, action)
