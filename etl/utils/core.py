from contextlib import contextmanager
from functools import wraps
from time import sleep

from elasticsearch import Elasticsearch
from psycopg2 import connect
from psycopg2.extras import DictCursor

from etl.utils.logger import get_logger
from etl.utils.settings import elastic


def backoff(start_sleep_time=0.1, factor=2, border_sleep_time=10):
    def func_wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            nonlocal start_sleep_time
            n = 0
            while True:
                try:
                    result = func(*args, **kwargs)
                except Exception as error:
                    if start_sleep_time < border_sleep_time:
                        start_sleep_time = start_sleep_time * (factor ** n)
                    else:
                        start_sleep_time = border_sleep_time
                    n += 1
                    get_logger().error(error)
                    sleep(start_sleep_time)
                else:
                    return result

        return inner

    return func_wrapper


@contextmanager
def connect_to_db(obj):
    @backoff()
    def db():
        return connect(**obj.dict(), cursor_factory=DictCursor)

    @backoff()
    def es():
        return Elasticsearch(hosts=elastic.elastic_url())

    result = db()
    result_ = es()

    try:
        yield {
            'postgres': result,
            'elastic': result_
        }
    finally:
        result.close()
        result_.close()
