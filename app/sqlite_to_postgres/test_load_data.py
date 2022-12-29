import sqlite3
from sqlite3 import Row

import psycopg2
from psycopg2.extras import DictCursor
from psycopg2.extensions import connection as _connection

from config.database import dsl, conn_sqlite
from utils.constants import TABLES

class Tests:

    def __init__(
            self,
            sqlite_connection: sqlite3.Connection,
            pg_connection: _connection
    ) -> None:
        self.sqlite_cur = sqlite_connection.cursor()
        self.pg_cur = pg_connection.cursor()

    def check_count(self, table: str) -> None:
        """Проверка на соответствие кол-ва записей в 2-ух БД"""
        stmt: str = '''
        SELECT COUNT (*) AS cnt FROM {0};
        '''.format(table)
        sqlite_row: Row = self.sqlite_cur.execute(stmt).fetchone()
        sqlite_count: dict[str, int] = dict(sqlite_row)
        pg_stmt: str = '''
        SELECT COUNT (*) FROM content.{0}
        '''.format(table)
        self.pg_cur.execute(pg_stmt)
        pg_count: dict[str, int] = dict(self.pg_cur.fetchone())
        assert sqlite_count['cnt'] == pg_count['count']

    def check_values(self, table):
        """Проверка на соответствие содержимого записей в 2-ух БД"""
        sqlite_stmt: str = "SELECT * FROM {0};".format(table)
        sqlite_select = self.sqlite_cur.execute(sqlite_stmt)
        for row in sqlite_select:
            sql_dict = dict(row)
            sql_dict.pop('created_at', None)
            sql_dict.pop('updated_at', None)
            pg_stmt = '''
            SELECT * FROM content.{0}
            WHERE id='{1}';
            '''.format(table, row['id'])
            self.pg_cur.execute(pg_stmt)
            pg_row = self.pg_cur.fetchone()
            pg_dict = dict(pg_row)
            pg_dict.pop('created_at', None)
            pg_dict.pop('updated_at', None)
            assert sql_dict == pg_dict

    def __call__(self, *args, **kwargs):
        for table in TABLES:
            self.check_count(table)
            self.check_values(table)


if __name__ == '__main__':

    with conn_sqlite(dsl['sqlite']['dbname']) as sqlite_conn,\
            psycopg2.connect(
                **dsl['postgres'],
                cursor_factory=DictCursor
            ) as pg_conn:
        sqlite_conn.row_factory = sqlite3.Row
        obj: Tests = Tests(sqlite_conn, pg_conn)
        obj()
