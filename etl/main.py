from psycopg2 import connect
from psycopg2.extras import DictCursor
from models import PostgreSQL
from qyeries import genres, persons


def main():
    obj = PostgreSQL()
    with connect(**obj.dict(), cursor_factory=DictCursor) as pg_conn:
        cur = pg_conn.cursor()
        query = genres % ''
        cur.execute(query)
        for i in cur:
            print(i)


if __name__ == '__main__':
    main()
