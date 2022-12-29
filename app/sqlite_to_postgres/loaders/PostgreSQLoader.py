from dataclasses import asdict, dataclass
from typing import Any

from psycopg2.extensions import connection, cursor

from models import TABLES
from utils import WrongValuesError


class PostgresSaver:

    def __init__(self, conn: connection):
        self.__cur: cursor = conn.cursor()

    def save_all_data(self, datas: tuple[str, list[Any]]):
        name_table: str = datas[0]
        datas_table: list[Any] = datas[1]
        for data in datas_table:
            try:
                data: dict[str, Any] = dict(data)
                obj: dataclass = TABLES[name_table](**data)
                if not obj:
                    raise WrongValuesError()
            except WrongValuesError as err:
                err()
                continue
            else:
                self._create_columns(name_table, obj)

    def _create_columns(self, table_name: str, data: dataclass):
        keys = asdict(data).keys()
        values = asdict(data).values()
        columns: str = ', '.join(keys)
        args: str = '%s, ' * len(keys)
        self.__cur.execute(
            f"""
            INSERT INTO content.{table_name} ({columns})
            VALUES ({args[:-2]});
            """, tuple(values),
        )
