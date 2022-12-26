from datetime import datetime

from psycopg2 import connect
from psycopg2.extras import DictCursor
from settings import PostgreSQL
from qyeries import genres, persons, film_work
from elasticsearch import Elasticsearch, helpers
from schema import mappings, settings


def main():
    obj = PostgreSQL()
    with connect(**obj.dict(), cursor_factory=DictCursor) as pg_conn:
        cur = pg_conn.cursor()
        query = genres % ''
        cur.execute(query)
        for i in cur:
            print(i)


if __name__ == '__main__':
    # main()
    es = Elasticsearch(hosts='http://localhost:9200/')

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

    helpers.bulk(es, action)
