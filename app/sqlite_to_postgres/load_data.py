"""Загрузка данных из БД."""


import logging
import sqlite3
from typing import Generator, Any

import psycopg2
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor

from config import dsl, conn_sqlite, logger
from loaders import PostgresSaver, SQLiteExtractor
from utils import WrongSaveError

logger()


def load_from_sqlite(
        connection: sqlite3.Connection,
        pg_conn: _connection,
):
    """Основной метод загрузки данных из SQLite в Postgres"""
    postgres_saver: PostgresSaver = PostgresSaver(pg_conn)
    sqlite_extractor: SQLiteExtractor = SQLiteExtractor(connection)

    datas: Generator[
        tuple[
            str,
            list[Any]
        ]
    ] = sqlite_extractor.extract_movies()
    for data in datas:
        logging.info('Перенос части записей в PostgreSQL.')
        try:
            postgres_saver.save_all_data(data)
        except WrongSaveError as err:
            logging.error(err)
            break


if __name__ == '__main__':
    logging.info('Запуск переноса данных.')
    with conn_sqlite(dsl['sqlite']['dbname'],) as sqlite_conn,\
            psycopg2.connect(
                **dsl['postgres'],
                cursor_factory=DictCursor,
            ) as pg_conn:
        sqlite_conn.row_factory = sqlite3.Row
        load_from_sqlite(sqlite_conn, pg_conn)
