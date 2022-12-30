import os
import logging
from time import sleep

from dotenv import load_dotenv

from load_data import Postgres, Elastic
from utils import connect_to_db, postgres, State, JsonFileStorage
from utils.settings import PostgresConfig


load_dotenv()


def build_storage():
    state: State = State(JsonFileStorage('results/file_path.json'))
    return state


def load_datas_from_psql_to_es():
    obj: PostgresConfig = postgres
    storage = build_storage()
    while True:
        with connect_to_db(obj) as db_base:
            logging.info('Подключение к базам данных прошло успешно')
            postgres_datas: Postgres = Postgres(db_base['postgres'], storage)
            elastics: Elastic = Elastic(db_base['elastic'])
            for data in postgres_datas():
                elastics.create_body_documents(data)
        print('all')
        sleep(int(os.getenv('TIME_TO_SLEEP')))


def main():
    load_datas_from_psql_to_es()


if __name__ == '__main__':
    main()
