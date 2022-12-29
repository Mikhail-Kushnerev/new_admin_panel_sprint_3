import json

from elasticsearch.helpers import bulk
from elasticsearch import NotFoundError

from utils.constants import DOCUMENT_BODY, INDEX_NAME
from utils.qyeries import first_film_work, genres, film_work, persons
from utils.schema import mappings, settings


class Postgres:
    def __init__(self, conn, storage, checkpoint=None):
        self.__cur = conn.cursor()
        self.start = 0
        self.checkpoint = checkpoint
        self.storage = storage
        self.mode = 'ASC'

    def take_first_film_work_date(self):
        query = first_film_work % self.mode
        self.__cur.execute(query)
        result = self.__cur.fetchone()
        date_first_film_work = result[0]
        return date_first_film_work

    def take_datas_by_date(self):
        for query in (persons, genres):
            self.__cur.execute(query % self.checkpoint)
            result = list(self.__cur)
            print(len(result))
            start, end, mid = 0, len(result), 50

            while start <= end:
                ids_coll = []

                for i in result[start: start + mid]:
                    ids_coll.append(i[0])

                self.start += len(ids_coll)
                start += mid
                yield ids_coll

    def take_film_works_by_needed_ids(self):
        for i in self.take_datas_by_date():
            query = film_work % str(tuple(i))
            self.__cur.execute(query)

            for j in self.__cur:
                target = dict(j)
                date = target.pop('updated_at')
                self.storage.set_state(
                    'finished part',
                    json.dumps(date, default=str)
                )
                yield target

    def __call__(self, *args, **kwargs):
        self.checkpoint = self.storage.get_state('finished part')
        if not self.checkpoint:
            self.checkpoint = self.take_first_film_work_date()
        for data in self.take_film_works_by_needed_ids():
            task = dict(data)
            yield task


class Elastic:
    def __init__(self, engine, datas=None):
        self.engine = engine
        self.datas = datas

    def check_exists_index(self):
        try:
            self.engine.indices.get(index=INDEX_NAME)
        except NotFoundError:
            self.engine.indices.create(
                index=INDEX_NAME,
                mappings=mappings,
                settings=settings
            )

    def create_body_documents(self, data):
        self.check_exists_index()
        DOCUMENT_BODY['_id'] = data['id']
        DOCUMENT_BODY['_source'] = data
        return self.create_document([DOCUMENT_BODY])

    def create_document(self, data):
        bulk(self.engine, data)
        self.engine.indices.refresh(index=INDEX_NAME)
