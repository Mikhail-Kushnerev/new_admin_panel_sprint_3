import logging
from time import sleep

from tqdm import tqdm

from load_data import Postgres, Elastic
from utils.core import connect_to_db
from utils.settings import postgres
from utils.storage import State, JsonFileStorage


def build_storage():
    state = State(JsonFileStorage('file_path.json'))
    return state


def load_datas_from_psql_to_es():
    obj, storage = postgres, build_storage()
    while True:
        with connect_to_db(obj) as db_base:
            logging.info('Подключение к базам данных прошло успешно')
            postgres_datas = Postgres(db_base['postgres'], storage)
            elastics = Elastic(db_base['elastic'])
            for data in tqdm(postgres_datas()):
                elastics.create_body_documents(data)
        sleep(1)


def main():
    load_datas_from_psql_to_es()


if __name__ == '__main__':
    main()
