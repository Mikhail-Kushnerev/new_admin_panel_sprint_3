import sqlite3

import psycopg2
from psycopg2.extras import DictCursor

from sqlite_to_postgres.utils import TABLES
from sqlite_to_postgres.config.database import dsl


def sqlite_connect():
    with sqlite3.connect(dsl['sqlite']['test']) as connect:
        connect.row_factory = sqlite3.Row
        cur = connect.cursor()
        yield cur


def postgresql_connect():
    with psycopg2.connect(
            **dsl['postgres'],
            cursor_factory=DictCursor
    ) as connect:
        cur = connect.cursor()
        yield cur


def count(db=None):
    query = '''SELECT {0} FROM {1}'''
    service = sqlite_connect()
    coll = []

    if db == 'postgresql':
        query = '''SELECT {0} FROM content.{1}'''
        service = postgresql_connect()
    for table in TABLES:
        for j in service:
            j.execute(query.format('COUNT (*)', table))
            coll.append(j.fetchone()[0])
    return coll


def test_count():
    assert count() == count('postgresql')


def values():
    sqlite = sqlite_connect()
    postgresql = postgresql_connect()
    for table in TABLES:
        for i in sqlite:
            datas = i.execute('SELECT * FROM {0}'.format(table))
            for row in datas:
                row = dict(row)
                row.pop('created_at')
                row.pop('updated_at')
                for j in postgresql:
                    j.execute(
                        '''
                        SELECT *
                        FROM content.{0}
                        WHERE id='{1}';
                        '''.format(table, row['id'])
                    )
                    result = dict(j.fetchone())
                    result.pop('created_at')
                    result.pop('updated_at')
                    yield result, row


def test_values():
    objects = values()
    for target in objects:
        assert target[0] == target[1]
