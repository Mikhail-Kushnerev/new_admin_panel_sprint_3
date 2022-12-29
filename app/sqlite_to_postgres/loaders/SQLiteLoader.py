import logging
from sqlite3 import Connection
from typing import Generator, Any

from models import TABLES
from utils.constants import PAGE_SIZE, DB_SIZE


class SQLiteExtractor:

    def __init__(
            self,
            conn: Connection,
    ) -> None:
        self.__cur: Connection.cursor = conn.cursor()

    def extract_movies(self):
        table_names: Generator[str] = self._check_tables()
        return self._send_datas(table_names)

    def _check_tables(self):
        self.__cur.execute(
            '''
            SELECT name
            FROM sqlite_master
            WHERE type='table';
            ''',
        )
        while True:
            tables: list = self.__cur.fetchmany(DB_SIZE)
            count_tables: int = self.size_datas(tables)
            if not count_tables:
                logging.info('Собраны названия всех таблиц.')
                break
            for table_name in tables:
                yield table_name

    def _send_datas(
            self,
            table
    ):
        for table_name in table:
            table_name: str = dict(table_name)['name']
            logging.info('Сбор записей таблицы {0}'.format(table_name))
            if self.validate_name(table_name):
                self.__cur.execute(
                    '''
                    SELECT * FROM {0}
                    '''.format(table_name),
                )
                while True:
                    table_datas: list = self.__cur.fetchmany(PAGE_SIZE)
                    length_table_datas: int = self.size_datas(table_datas)
                    if not length_table_datas:
                        logging.info(
                            'Собраны все записи таблицы {0}'.format(
                                table_name
                            )
                        )
                        break
                    yield table_name, table_datas

    @staticmethod
    def validate_name(table_name: str):
        return TABLES[table_name] if table_name in TABLES else False

    @staticmethod
    def size_datas(datas: list[Any]):
        return len(datas)
