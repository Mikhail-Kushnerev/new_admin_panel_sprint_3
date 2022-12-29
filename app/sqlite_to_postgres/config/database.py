import os
import sqlite3
from contextlib import contextmanager

from dotenv import load_dotenv

load_dotenv()


@contextmanager
def conn_sqlite(db_path: str):
    conn: sqlite3.Connection = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    yield conn
    conn.close()


dsl: dict[str, dict[str | int]] = {
    'postgres': {
        'dbname': os.getenv('POSTGRES_DB', default='postgres'),
        'user': os.getenv('POSTGRES_USER', default='postgres'),
        'password': os.getenv('POSTGRES_PASSWORD', default='postgres'),
        'host': os.getenv('POSTGRES_HOST', default='127.0.0.1'),
        'port': os.getenv('POSTGRES_PORT', default=5432),
    },
    'sqlite': {
        'dbname': os.getenv('ORIGINAL_DB', default='sqlite.db'),
        'test': os.getenv('TEST_DB'),
    },
}
