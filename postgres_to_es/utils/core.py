from contextlib import contextmanager
from functools import wraps
from time import sleep
from typing import Callable

from elasticsearch import Elasticsearch
from psycopg2 import connect
from psycopg2.extras import DictCursor
from psycopg2.extensions import connection

from utils import get_logger, elastic
from .settings import PostgresConfig


def backoff(
        start_sleep_time=0.1,
        *,
        factor: int = 2,
        border_sleep_time: int = 10
) -> Callable:
    def func_wrapper(func: Callable) -> Callable:
        @wraps(func)
        def inner(*args, **kwargs) -> Callable:
            nonlocal start_sleep_time
            n: int = 0
            while True:
                try:
                    return func(*args, **kwargs)
                except Exception as error:
                    if start_sleep_time < border_sleep_time:
                        start_sleep_time = start_sleep_time * (factor ** n)
                    else:
                        start_sleep_time = border_sleep_time
                    n += 1
                    get_logger().error(error)
                    sleep(start_sleep_time)

        return inner

    return func_wrapper


@contextmanager
def connect_to_db(obj: PostgresConfig):
    @backoff()
    def db() -> connection:
        return connect(**obj.dict(), cursor_factory=DictCursor)

    @backoff()
    def es() -> Elasticsearch:
        es_conn: Elasticsearch = Elasticsearch(hosts=elastic.elastic_url())
        es_conn.info()
        return es_conn

    result: connection = db()
    result_: Elasticsearch = es()

    try:
        yield {
            'postgres': result,
            'elastic': result_
        }
    finally:
        result.close()
        result_.close()
