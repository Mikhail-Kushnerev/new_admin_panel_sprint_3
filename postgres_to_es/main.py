import logging

from tqdm import tqdm

from load_data import Postgres, Elastic
from utils.core import connect_to_db
# from utils.logger import get_logger
from utils.settings import postgres
from utils.storage import State, JsonFileStorage


def build_storage():
    state = State(JsonFileStorage('file_path.json'))
    return state


def load_datas_from_psql_to_es():
    obj, storage = postgres, build_storage()
    conn = connect_to_db(obj)
    with conn as db_base:
        logging.info('Подключение к базам данных прошло успешно')
        postgres_datas = Postgres(db_base['postgres'], storage)
        elastics = Elastic(db_base['elastic'])
        for data in tqdm(postgres_datas()):
            elastics.create_body_documents(data)


def main():
    # get_logger()
    load_datas_from_psql_to_es()


if __name__ == '__main__':
    # get_logger()
    main()
